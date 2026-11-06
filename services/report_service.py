class ReportService:
    def __init__(self, db):
        self.db = db

    def available_equipment(self) -> list:
        return self.db.query(
            "SELECT e.equipment_id, e.name, e.category, "
            "e.quantity - COALESCE(SUM(l.quantity), 0) AS available "
            "FROM equipment e "
            "LEFT JOIN loans l ON l.equipment_id = e.equipment_id "
            "AND l.returned_on IS NULL "
            "GROUP BY e.equipment_id "
            "ORDER BY e.equipment_id")

    def outstanding_loans(self) -> list:
        return self.db.query(
            "SELECT l.loan_id, l.member_id, m.name AS member_name, "
            "l.equipment_id, e.name AS equipment_name, l.quantity, l.borrowed_on "
            "FROM loans l "
            "JOIN members m ON m.member_id = l.member_id "
            "JOIN equipment e ON e.equipment_id = l.equipment_id "
            "WHERE l.returned_on IS NULL "
            "ORDER BY l.loan_id")

    def most_borrowed_equipment(self) -> list:
        return self.db.query(
            "SELECT e.equipment_id, e.name, e.category, "
            "COALESCE(SUM(l.quantity), 0) AS times_borrowed "
            "FROM equipment e "
            "LEFT JOIN loans l ON l.equipment_id = e.equipment_id "
            "GROUP BY e.equipment_id "
            "ORDER BY times_borrowed DESC, e.name")

    def members_with_outstanding_loans(self) -> list:
        return self.db.query(
            "SELECT m.member_id, m.name, m.contact, COUNT(l.loan_id) AS open_loans "
            "FROM members m "
            "JOIN loans l ON l.member_id = m.member_id "
            "WHERE l.returned_on IS NULL "
            "GROUP BY m.member_id "
            "ORDER BY m.member_id")

    def summary(self) -> dict:
        total_equipment = self.db.query_one(
            "SELECT COUNT(*) AS c FROM equipment")["c"]
        total_members = self.db.query_one(
            "SELECT COUNT(*) AS c FROM members")["c"]
        outstanding = self.db.query_one(
            "SELECT COUNT(*) AS c FROM loans WHERE returned_on IS NULL")["c"]
        return {"equipment": total_equipment, "members": total_members,
                "outstanding_loans": outstanding}