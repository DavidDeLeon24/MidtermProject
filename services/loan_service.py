from datetime import date
from models import Loan

class LoanService:
    def __init__(self, db, equipment_service, member_service):
        self.con = db.con
        self.equipment_service = equipment_service
        self.member_service = member_service

    def lend_equipment(self, member_id, equipment_id, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
            
        # Check if member exists
        if self.member_service.get_member(member_id) is None:
            raise ValueError("Member does not exist.")
            
        # Check if equipment exists
        if self.equipment_service.get_equipment(equipment_id) is None:
            raise ValueError("Equipment does not exist.")
            
        # Check availability
        available = self.equipment_service.available_quantity(equipment_id)
        if available < quantity:
            raise ValueError("Insufficient equipment. Available: " + str(available))
            
        # Record the loan
        today = date.today().isoformat()
        cur = self.con.cursor()
        cur.execute("INSERT INTO loans (member_id, equipment_id, quantity, borrowed_on) VALUES (?, ?, ?, ?)", (member_id, equipment_id, quantity, today))
        self.con.commit()
        return cur.lastrowid

    def return_loan(self, loan_id):
        cur = self.con.cursor()
        cur.execute("SELECT returned_on FROM loans WHERE loan_id = ?", (loan_id,))
        row = cur.fetchone()
        
        if row is None:
            raise ValueError("Loan does not exist.")
            
        if row[0] is not None:
            raise ValueError("This loan has already been returned.")
            
        today = date.today().isoformat()
        cur.execute("UPDATE loans SET returned_on = ? WHERE loan_id = ?", (today, loan_id))
        self.con.commit()

    def loans_for_member(self, member_id):
        cur = self.con.cursor()
        cur.execute("SELECT loan_id, member_id, equipment_id, quantity, borrowed_on, returned_on FROM loans WHERE member_id = ? ORDER BY loan_id", (member_id,))
        rows = cur.fetchall()
        
        loans = []
        for row in rows:
            l = Loan(row[0], row[1], row[2], row[3], row[4], row[5])
            loans.append(l)
        return loans

    def outstanding_loans(self):
        cur = self.con.cursor()
        cur.execute("SELECT loan_id, member_id, equipment_id, quantity, borrowed_on, returned_on FROM loans WHERE returned_on IS NULL ORDER BY loan_id")
        rows = cur.fetchall()
        
        loans = []
        for row in rows:
            l = Loan(row[0], row[1], row[2], row[3], row[4], row[5])
            loans.append(l)
        return loans