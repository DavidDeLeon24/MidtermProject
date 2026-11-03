"""Member domain object."""


class Member:
    def __init__(self, member_id, name, contact):
        self.member_id = member_id
        self.name = name
        self.contact = contact

    def __str__(self):
        return f"{self.member_id}: {self.name} | {self.contact}"