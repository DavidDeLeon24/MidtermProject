"""Loan domain object."""


class Loan:
    def __init__(self, loan_id, member_id, equipment_id, quantity,
                 borrowed_on, returned_on=None):
        self.loan_id = loan_id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.quantity = quantity
        self.borrowed_on = borrowed_on
        self.returned_on = returned_on

    @property
    def is_open(self) -> bool:
        return self.returned_on is None

    def __str__(self):
        status = "OUT" if self.is_open else f"returned {self.returned_on}"
        return (f"Loan #{self.loan_id}: member={self.member_id}, "
                f"equipment={self.equipment_id}, qty={self.quantity}, "
                f"borrowed={self.borrowed_on} ({status})")