class Loan:
    def __init__(self, loan_id, member_id, equipment_id, quantity, borrowed_on, returned_on=None):
        self.loan_id = loan_id
        self.member_id = member_id
        self.equipment_id = equipment_id
        self.quantity = quantity
        self.borrowed_on = borrowed_on
        self.returned_on = returned_on