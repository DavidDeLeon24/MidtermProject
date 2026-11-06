from datetime import date

from models.loan import Loan


class LoanService:
    def __init__(self, db, equipment_service, member_service):
        self.db = db
        self.equipment_service = equipment_service
        self.member_service = member_service

    def _to_model(self, row) -> Loan:
        return Loan(row["loan_id"], row["member_id"], row["equipment_id"],
                    row["quantity"], row["borrowed_on"], row["returned_on"])

    def lend_equipment(self, member_id: str, equipment_id: int,
                       quantity: int) -> Loan:
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        if not self.member_service.get_member(member_id):
            raise ValueError("Member does not exist.")
        if not self.equipment_service.get_equipment(equipment_id):
            raise ValueError("Equipment does not exist.")
        available = self.equipment_service.available_quantity(equipment_id)
        if available < quantity:
            raise ValueError(f"Insufficient equipment. Available: {available}.")
        borrowed_on = date.today().isoformat()
        cur = self.db.execute(
            "INSERT INTO loans (member_id, equipment_id, quantity, borrowed_on) "
            "VALUES (?, ?, ?, ?)",
            (member_id, equipment_id, quantity, borrowed_on))
        return Loan(cur.lastrowid, member_id, equipment_id, quantity, borrowed_on)

    def return_loan(self, loan_id: int) -> None:
        row = self.db.query_one(
            "SELECT loan_id, returned_on FROM loans WHERE loan_id = ?", (loan_id,))
        if not row:
            raise ValueError("Loan does not exist.")
        if row["returned_on"] is not None:
            raise ValueError("This loan has already been returned.")
        returned_on = date.today().isoformat()
        self.db.execute("UPDATE loans SET returned_on = ? WHERE loan_id = ?",
                        (returned_on, loan_id))

    def loans_for_member(self, member_id: str) -> list:
        rows = self.db.query(
            "SELECT loan_id, member_id, equipment_id, quantity, borrowed_on, "
            "returned_on FROM loans WHERE member_id = ? ORDER BY loan_id",
            (member_id,))
        return [self._to_model(r) for r in rows]

    def outstanding_loans(self) -> list:
        rows = self.db.query(
            "SELECT loan_id, member_id, equipment_id, quantity, borrowed_on, "
            "returned_on FROM loans WHERE returned_on IS NULL ORDER BY loan_id")
        return [self._to_model(r) for r in rows]

    def get_loan(self, loan_id: int):
        row = self.db.query_one(
            "SELECT loan_id, member_id, equipment_id, quantity, borrowed_on, "
            "returned_on FROM loans WHERE loan_id = ?", (loan_id,))
        return self._to_model(row) if row else None