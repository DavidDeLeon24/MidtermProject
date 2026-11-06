from models.equipment import Equipment


class EquipmentService:
    def __init__(self, db):
        self.db = db

    def _to_model(self, row) -> Equipment:
        return Equipment(row["equipment_id"], row["name"],
                         row["category"], row["quantity"])

    def add_equipment(self, name: str, category: str, quantity: int) -> Equipment:
        name = name.strip()
        category = category.strip()
        if not name or not category:
            raise ValueError("Name and category are required.")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        existing = self.db.query_one(
            "SELECT equipment_id FROM equipment WHERE name = ? AND category = ?",
            (name, category))
        if existing:
            raise ValueError("Equipment with this name and category already exists.")
        cur = self.db.execute(
            "INSERT INTO equipment (name, category, quantity) VALUES (?, ?, ?)",
            (name, category, quantity))
        return Equipment(cur.lastrowid, name, category, quantity)

    def list_equipment(self) -> list:
        rows = self.db.query(
            "SELECT equipment_id, name, category, quantity FROM equipment "
            "ORDER BY equipment_id")
        return [self._to_model(r) for r in rows]

    def get_equipment(self, equipment_id: int):
        row = self.db.query_one(
            "SELECT equipment_id, name, category, quantity FROM equipment "
            "WHERE equipment_id = ?", (equipment_id,))
        return self._to_model(row) if row else None

    def search(self, term: str) -> list:
        term = f"%{term.strip()}%"
        rows = self.db.query(
            "SELECT equipment_id, name, category, quantity FROM equipment "
            "WHERE name LIKE ? OR category LIKE ? ORDER BY equipment_id",
            (term, term))
        return [self._to_model(r) for r in rows]

    def update_equipment(self, equipment_id: int, name=None, category=None,
                         quantity=None) -> None:
        current = self.get_equipment(equipment_id)
        if not current:
            raise ValueError("Equipment not found.")
        new_name = current.name if name is None else name.strip()
        new_category = current.category if category is None else category.strip()
        new_quantity = current.quantity if quantity is None else quantity
        if not new_name or not new_category:
            raise ValueError("Name and category cannot be empty.")
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative.")
        duplicate = self.db.query_one(
            "SELECT equipment_id FROM equipment WHERE name = ? AND category = ? "
            "AND equipment_id <> ?",
            (new_name, new_category, equipment_id))
        if duplicate:
            raise ValueError("Another equipment with this name and category exists.")
        self.db.execute(
            "UPDATE equipment SET name = ?, category = ?, quantity = ? "
            "WHERE equipment_id = ?",
            (new_name, new_category, new_quantity, equipment_id))

    def remove_equipment(self, equipment_id: int) -> None:
        current = self.get_equipment(equipment_id)
        if not current:
            raise ValueError("Equipment not found.")
        open_loan = self.db.query_one(
            "SELECT loan_id FROM loans WHERE equipment_id = ? AND returned_on IS NULL",
            (equipment_id,))
        if open_loan:
            raise ValueError("Cannot remove equipment with outstanding loans.")
        self.db.execute("DELETE FROM equipment WHERE equipment_id = ?",
                        (equipment_id,))

    def available_quantity(self, equipment_id: int) -> int:
        row = self.db.query_one(
            "SELECT e.quantity - COALESCE(SUM(l.quantity), 0) AS available "
            "FROM equipment e "
            "LEFT JOIN loans l ON l.equipment_id = e.equipment_id "
            "AND l.returned_on IS NULL "
            "WHERE e.equipment_id = ? GROUP BY e.equipment_id",
            (equipment_id,))
        if not row:
            return 0
        return row["available"] if row["available"] is not None else 0