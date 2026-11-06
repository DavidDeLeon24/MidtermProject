from utils import ask_int, ask_non_empty

class LoanMenu:
    def __init__(self, loan_service, equipment_service):
        self.service = loan_service
        self.equipment_service = equipment_service

    def run(self):
        while True:
            print("\n--- Lending & Returns ---")
            print("1. Lend equipment to a member")
            print("2. Return equipment")
            print("3. Show current loans for a member")
            print("4. Show all outstanding loans")
            print("0. Back")
            choice = input("Choice: ").strip()
            
            if choice == "1":
                self.lend()
            elif choice == "2":
                self.return_equipment()
            elif choice == "3":
                self.member_loans()
            elif choice == "4":
                self.all_outstanding()
            elif choice == "0":
                return
            else:
                print("  ! Invalid option.")

    def lend(self):
        mid = ask_non_empty("Member ID: ")
        eq_id = ask_int("Equipment ID: ")
        
        eq = self.equipment_service.get_equipment(eq_id)
        if eq is None:
            print("  ! Equipment not found.")
            return
            
        avail = self.equipment_service.available_quantity(eq_id)
        print("  Available to lend: " + str(avail) + " of " + str(eq.quantity) + " owned.")
        
        qty = ask_int("Quantity: ")
        try:
            loan_id = self.service.lend_equipment(mid, eq_id, qty)
            print("  Loan #" + str(loan_id) + " recorded.")
        except ValueError as e:
            print("  ! Error: " + str(e))

    def return_equipment(self):
        loan_id = ask_int("Loan ID to return: ")
        try:
            self.service.return_loan(loan_id)
            print("  Loan #" + str(loan_id) + " marked as returned.")
        except ValueError as e:
            print("  ! Error: " + str(e))

    def member_loans(self):
        mid = ask_non_empty("Member ID: ")
        loans = self.service.loans_for_member(mid)
        if not loans:
            print("  (no loans for this member)")
        else:
            for l in loans:
                status = "OUT"
                if l.returned_on is not None:
                    status = "returned " + l.returned_on
                print("  Loan #" + str(l.loan_id) + ": Equipment ID " + str(l.equipment_id) + ", Qty " + str(l.quantity) + ", Borrowed " + l.borrowed_on + " (" + status + ")")

    def all_outstanding(self):
        loans = self.service.outstanding_loans()
        if not loans:
            print("  (no outstanding loans)")
        else:
            for l in loans:
                print("  Loan #" + str(l.loan_id) + ": Member " + l.member_id + ", Equipment ID " + str(l.equipment_id) + ", Qty " + str(l.quantity) + ", Borrowed " + l.borrowed_on)