import sqlite3

class Database:
    def __init__(self):
        # Connect to the database file
        self.con = sqlite3.connect("lending.db")
        self.create_tables()

    def create_tables(self):
        cur = self.con.cursor()
        
        # Create equipment table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS equipment (
                equipment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        """)
        
        # Create members table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)
        
        # Create loans table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id TEXT NOT NULL,
                equipment_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                borrowed_on TEXT NOT NULL,
                returned_on TEXT,
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (equipment_id) REFERENCES equipment(equipment_id)
            )
        """)
        self.con.commit()

    def close(self):
        self.con.close()