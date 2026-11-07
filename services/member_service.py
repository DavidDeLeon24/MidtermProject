from models import Member

class MemberService:
    def __init__(self, db):
        self.con = db.con

    def register_member(self, member_id, name, contact):
        cur = self.con.cursor()
        
        # Check for duplicate ID
        cur.execute("SELECT member_id FROM members WHERE member_id = ?", (member_id,))
        if cur.fetchone() is not None:
            raise ValueError("A member with this ID already exists.")
            
        cur.execute("INSERT INTO members (member_id, name, contact) VALUES (?, ?, ?)", (member_id, name, contact))
        self.con.commit()

    def list_members(self):
        cur = self.con.cursor()
        cur.execute("SELECT member_id, name, contact FROM members ORDER BY member_id")
        rows = cur.fetchall()
        
        member_list = []
        for row in rows:
            m = Member(row[0], row[1], row[2])
            member_list.append(m)
        return member_list

    def get_member(self, member_id):
        cur = self.con.cursor()
        cur.execute("SELECT member_id, name, contact FROM members WHERE member_id = ?", (member_id,))
        row = cur.fetchone()
        
        if row is None:
            return None
        return Member(row[0], row[1], row[2])

    def update_member(self, member_id, name, contact):
        cur = self.con.cursor()
        cur.execute("UPDATE members SET name = ?, contact = ? WHERE member_id = ?", (name, contact, member_id))
        self.con.commit()