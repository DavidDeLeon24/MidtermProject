from models import Equipment

class EquipmentService:
    def __init__(self, db):
        self.con = db.con

    def add_equipment(self, name, category, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
            
        cur = self.con.cursor()
        # Check for duplicates using standard tuple fetching
        cur.execute("SELECT equipment_id FROM equipment WHERE name = ? AND category = ?", (name, category))
        if cur.fetchone() is not None:
            raise ValueError("Equipment with this name and category already exists.")
            
        cur.execute("INSERT INTO equipment (name, category, quantity) VALUES (?, ?, ?)", (name, category, quantity))
        self.con.commit()
        return cur.lastrowid

    def list_equipment(self):
        cur = self.con.cursor()
        cur.execute("SELECT equipment_id, name, category, quantity FROM equipment ORDER BY equipment_id")
        rows = cur.fetchall()
        
        equipment_list = []
        for row in rows:
            eq = Equipment(row[0], row[1], row[2], row[3])
            equipment_list.append(eq)
        return equipment_list

    def get_equipment(self, equipment_id):
        cur = self.con.cursor()
        cur.execute("SELECT equipment_id, name, category, quantity FROM equipment WHERE equipment_id = ?", (equipment_id,))
        row = cur.fetchone()
        
        if row is None:
            return None
        return Equipment(row[0], row[1], row[2], row[3])

    def search_equipment(self, term):
        cur = self.con.cursor()
        search_term = "%" + term + "%"
        cur.execute("SELECT equipment_id, name, category, quantity FROM equipment WHERE name LIKE ? OR category LIKE ?", (search_term, search_term))
        rows = cur.fetchall()
        
        results = []
        for row in rows:
            results.append(Equipment(row[0], row[1], row[2], row[3]))
        return results

    def update_equipment(self, equipment_id, name, category, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative.")
            
        cur = self.con.cursor()
        cur.execute("UPDATE equipment SET name = ?, category = ?, quantity = ? WHERE equipment_id = ?", (name, category, quantity, equipment_id))
        self.con.commit()

    def remove_equipment(self, equipment_id):
        cur = self.con.cursor()
        cur.execute("SELECT loan_id FROM loans WHERE equipment_id = ? AND returned_on IS NULL", (equipment_id,))
        if cur.fetchone() is not None:
            raise ValueError("Cannot remove equipment with outstanding loans.")
            
        cur.execute("DELETE FROM equipment WHERE equipment_id = ?", (equipment_id,))
        self.con.commit()

    def available_quantity(self, equipment_id):
        cur = self.con.cursor()
        
        # Get total quantity
        cur.execute("SELECT quantity FROM equipment WHERE equipment_id = ?", (equipment_id,))
        row = cur.fetchone()
        if row is None:
            return 0
        total_owned = row[0]
        
        # Get how many are currently on loan
        cur.execute("SELECT quantity FROM loans WHERE equipment_id = ? AND returned_on IS NULL", (equipment_id,))
        loan_rows = cur.fetchall()
        
        total_on_loan = 0
        for l_row in loan_rows:
            total_on_loan = total_on_loan + l_row[0]
            
        return total_owned - total_on_loan