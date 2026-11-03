"""
database.py
------------
Handles the SQLite connection, schema creation, and shared helpers.

Design notes:
- One connection object is created at startup and shared by services.
- Foreign keys are enabled so that ON DELETE / ON UPDATE rules work.
- Tables are created automatically if they do not exist.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "lending.sqlite")


class Database:
    """Thin wrapper around a sqlite3 connection."""

    def __init__(self, path: str = DB_PATH):
        self.path = path
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row       # dict-like access
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._create_schema()

    # ----------------------------------------------------------
    def _create_schema(self) -> None:
        """Create tables if they do not exist."""
        cur = self.conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS equipment (
                equipment_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                category      TEXT    NOT NULL,
                quantity      INTEGER NOT NULL CHECK (quantity >= 0),
                UNIQUE (name, category)
            );

            CREATE TABLE IF NOT EXISTS members (
                member_id     TEXT    PRIMARY KEY,
                name          TEXT    NOT NULL,
                contact       TEXT    NOT NULL
            );

            CREATE TABLE IF NOT EXISTS loans (
                loan_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id     TEXT    NOT NULL,
                equipment_id  INTEGER NOT NULL,
                quantity      INTEGER NOT NULL CHECK (quantity > 0),
                borrowed_on   TEXT    NOT NULL,   -- ISO date
                returned_on   TEXT,               -- NULL = still out
                FOREIGN KEY (member_id)    REFERENCES members(member_id)
                    ON UPDATE CASCADE ON DELETE RESTRICT,
                FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            );
            """
        )
        self.conn.commit()

    # ----------------------------------------------------------
    def execute(self, sql: str, params: tuple = ()):
        """Run a parameterized INSERT/UPDATE/DELETE and commit."""
        cur = self.conn.execute(sql, params)
        self.conn.commit()
        return cur

    def query(self, sql: str, params: tuple = ()):
        """Run a parameterized SELECT and return all rows."""
        return self.conn.execute(sql, params).fetchall()

    def query_one(self, sql: str, params: tuple = ()):
        return self.conn.execute(sql, params).fetchone()

    def close(self) -> None:
        self.conn.close()