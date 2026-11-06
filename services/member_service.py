from models.member import Member


class MemberService:
    def __init__(self, db):
        self.db = db

    def _to_model(self, row) -> Member:
        return Member(row["member_id"], row["name"], row["contact"])

    def register_member(self, member_id: str, name: str, contact: str) -> Member:
        member_id = member_id.strip()
        name = name.strip()
        contact = contact.strip()
        if not member_id or not name or not contact:
            raise ValueError("Member ID, name and contact are required.")
        existing = self.db.query_one(
            "SELECT member_id FROM members WHERE member_id = ?", (member_id,))
        if existing:
            raise ValueError("A member with this ID already exists.")
        self.db.execute(
            "INSERT INTO members (member_id, name, contact) VALUES (?, ?, ?)",
            (member_id, name, contact))
        return Member(member_id, name, contact)

    def list_members(self) -> list:
        rows = self.db.query(
            "SELECT member_id, name, contact FROM members ORDER BY member_id")
        return [self._to_model(r) for r in rows]

    def get_member(self, member_id: str):
        row = self.db.query_one(
            "SELECT member_id, name, contact FROM members WHERE member_id = ?",
            (member_id,))
        return self._to_model(row) if row else None

    def update_member(self, member_id: str, name=None, contact=None) -> None:
        current = self.get_member(member_id)
        if not current:
            raise ValueError("Member not found.")
        new_name = current.name if name is None else name.strip()
        new_contact = current.contact if contact is None else contact.strip()
        if not new_name or not new_contact:
            raise ValueError("Name and contact cannot be empty.")
        self.db.execute(
            "UPDATE members SET name = ?, contact = ? WHERE member_id = ?",
            (new_name, new_contact, member_id))