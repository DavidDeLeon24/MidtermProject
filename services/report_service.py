class ReportService:
    def __init__(self, db):
        self.con = db.con

    def available_equipment(self):
        cur = self.con.cursor()
        cur.execute("SELECT equipment_id, name, category, quantity FROM equipment")
        eq_rows = cur.fetchall()
        
        results = []
        for row in eq_rows:
            eid = row[0]
            name = row[1]
            category = row[2]
            total = row[3]
            
            # Get open loans for this equipment
            cur.execute("SELECT quantity FROM loans WHERE equipment_id = ? AND returned_on IS NULL", (eid,))
            loan_rows = cur.fetchall()
            loaned = 0
            for l_row in loan_rows:
                loaned = loaned + l_row[0]
                
            available = total - loaned
            if available > 0:
                # Append as a dictionary
                results.append({"id": eid, "name": name, "category": category, "available": available})
        return results

    def outstanding_loans(self):
        cur = self.con.cursor()
        # Basic join query
        cur.execute("""
            SELECT l.loan_id, l.member_id, m.name, l.equipment_id, e.name, l.quantity, l.borrowed_on
            FROM loans l
            JOIN members m ON m.member_id = l.member_id
            JOIN equipment e ON e.equipment_id = l.equipment_id
            WHERE l.returned_on IS NULL
        """)
        return cur.fetchall()

    def most_borrowed_equipment(self):
        cur = self.con.cursor()
        cur.execute("SELECT equipment_id, name, category FROM equipment")
        eq_rows = cur.fetchall()
        
        report_data = []
        for row in eq_rows:
            eid = row[0]
            name = row[1]
            category = row[2]
            
            cur.execute("SELECT quantity FROM loans WHERE equipment_id = ?", (eid,))
            loan_rows = cur.fetchall()
            total_borrowed = 0
            for l_row in loan_rows:
                total_borrowed = total_borrowed + l_row[0]
                
            report_data.append({"name": name, "category": category, "times_borrowed": total_borrowed})
            
        # Simple bubble sort to sort by times_borrowed descending
        for i in range(len(report_data)):
            for j in range(0, len(report_data) - i - 1):
                if report_data[j]["times_borrowed"] < report_data[j+1]["times_borrowed"]:
                    temp = report_data[j]
                    report_data[j] = report_data[j+1]
                    report_data[j+1] = temp
                    
        return report_data

    def members_with_outstanding_loans(self):
        cur = self.con.cursor()
        cur.execute("""
            SELECT m.member_id, m.name, COUNT(l.loan_id)
            FROM members m
            JOIN loans l ON l.member_id = m.member_id
            WHERE l.returned_on IS NULL
            GROUP BY m.member_id
        """)
        return cur.fetchall()

    def summary(self):
        cur = self.con.cursor()
        
        cur.execute("SELECT COUNT(*) FROM equipment")
        total_eq = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM members")
        total_mem = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM loans WHERE returned_on IS NULL")
        open_loans = cur.fetchone()[0]
        
        return {"equipment": total_eq, "members": total_mem, "outstanding_loans": open_loans}