from database import Database
from services import EquipmentService, MemberService, LoanService, ReportService


def prompt(text: str) -> str:
    return input(text).strip()


def read_int(text: str) -> int:
    try:
        return int(prompt(text))
    except ValueError:
        raise ValueError("Please enter a valid integer.")


def equipment_menu(service: EquipmentService) -> None:
    while True:
        print("\n--- Equipment Management ---")
        print("1. Register equipment")
        print("2. List all equipment")
        print("3. Search equipment")
        print("4. Update equipment")
        print("5. Remove equipment")
        print("0. Back")
        choice = prompt("Choose: ")
        try:
            if choice == "1":
                name = prompt("Name: ")
                category = prompt("Category: ")
                quantity = read_int("Quantity: ")
                eq = service.add_equipment(name, category, quantity)
                print(f"Registered: {eq}")
            elif choice == "2":
                items = service.list_equipment()
                if not items:
                    print("No equipment registered.")
                for eq in items:
                    print(eq)
            elif choice == "3":
                term = prompt("Search name or category: ")
                results = service.search(term)
                if not results:
                    print("No matches.")
                for eq in results:
                    print(eq)
            elif choice == "4":
                equipment_id = read_int("Equipment ID: ")
                name = prompt("New name (blank to keep): ")
                category = prompt("New category (blank to keep): ")
                qty_text = prompt("New quantity (blank to keep): ")
                quantity = int(qty_text) if qty_text else None
                service.update_equipment(equipment_id,
                                         name if name else None,
                                         category if category else None,
                                         quantity)
                print("Equipment updated.")
            elif choice == "5":
                equipment_id = read_int("Equipment ID: ")
                service.remove_equipment(equipment_id)
                print("Equipment removed.")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


def member_menu(service: MemberService) -> None:
    while True:
        print("\n--- Member Management ---")
        print("1. Register member")
        print("2. List all members")
        print("3. Search member by ID")
        print("4. Update member")
        print("0. Back")
        choice = prompt("Choose: ")
        try:
            if choice == "1":
                member_id = prompt("Member ID: ")
                name = prompt("Name: ")
                contact = prompt("Contact: ")
                m = service.register_member(member_id, name, contact)
                print(f"Registered: {m}")
            elif choice == "2":
                members = service.list_members()
                if not members:
                    print("No members registered.")
                for m in members:
                    print(m)
            elif choice == "3":
                member_id = prompt("Member ID: ")
                m = service.get_member(member_id)
                print(m if m else "Member not found.")
            elif choice == "4":
                member_id = prompt("Member ID: ")
                name = prompt("New name (blank to keep): ")
                contact = prompt("New contact (blank to keep): ")
                service.update_member(member_id,
                                      name if name else None,
                                      contact if contact else None)
                print("Member updated.")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


def loan_menu(service: LoanService) -> None:
    while True:
        print("\n--- Lending and Returns ---")
        print("1. Lend equipment")
        print("2. Return equipment")
        print("3. Loans for a member")
        print("4. All outstanding loans")
        print("0. Back")
        choice = prompt("Choose: ")
        try:
            if choice == "1":
                member_id = prompt("Member ID: ")
                equipment_id = read_int("Equipment ID: ")
                quantity = read_int("Quantity: ")
                loan = service.lend_equipment(member_id, equipment_id, quantity)
                print(f"Loan recorded: {loan}")
            elif choice == "2":
                loan_id = read_int("Loan ID: ")
                service.return_loan(loan_id)
                print("Return recorded.")
            elif choice == "3":
                member_id = prompt("Member ID: ")
                loans = service.loans_for_member(member_id)
                if not loans:
                    print("No loans for this member.")
                for loan in loans:
                    print(loan)
            elif choice == "4":
                loans = service.outstanding_loans()
                if not loans:
                    print("No outstanding loans.")
                for loan in loans:
                    print(loan)
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except ValueError as exc:
            print(f"Error: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


def report_menu(service: ReportService) -> None:
    while True:
        print("\n--- Reports ---")
        print("1. Available equipment")
        print("2. Outstanding loans")
        print("3. Most borrowed equipment")
        print("4. Members with outstanding loans")
        print("5. Summary")
        print("0. Back")
        choice = prompt("Choose: ")
        try:
            if choice == "1":
                print("\nAvailable equipment:")
                for row in service.available_equipment():
                    print(f"[{row['equipment_id']}] {row['name']} "
                          f"({row['category']}) - available: {row['available']}")
            elif choice == "2":
                print("\nOutstanding loans:")
                for row in service.outstanding_loans():
                    print(f"Loan #{row['loan_id']}: {row['member_id']} "
                          f"({row['member_name']}) borrowed "
                          f"{row['quantity']} x {row['equipment_name']} "
                          f"on {row['borrowed_on']}")
            elif choice == "3":
                print("\nMost borrowed equipment:")
                for row in service.most_borrowed_equipment():
                    print(f"[{row['equipment_id']}] {row['name']} "
                          f"({row['category']}) - borrowed: {row['times_borrowed']}")
            elif choice == "4":
                print("\nMembers with outstanding loans:")
                for row in service.members_with_outstanding_loans():
                    print(f"{row['member_id']}: {row['name']} | "
                          f"{row['contact']} | open loans: {row['open_loans']}")
            elif choice == "5":
                s = service.summary()
                print(f"\nTotal equipment: {s['equipment']}")
                print(f"Total members:   {s['members']}")
                print(f"Outstanding loans: {s['outstanding_loans']}")
            elif choice == "0":
                return
            else:
                print("Invalid choice.")
        except Exception as exc:
            print(f"Unexpected error: {exc}")


def main() -> None:
    db = Database()
    equipment_service = EquipmentService(db)
    member_service = MemberService(db)
    loan_service = LoanService(db, equipment_service, member_service)
    report_service = ReportService(db)
    try:
        while True:
            print("\n===== Equipment Lending Management System =====")
            print("1. Equipment management")
            print("2. Member management")
            print("3. Lending and returns")
            print("4. Reports")
            print("0. Exit")
            choice = prompt("Choose: ")
            if choice == "1":
                equipment_menu(equipment_service)
            elif choice == "2":
                member_menu(member_service)
            elif choice == "3":
                loan_menu(loan_service)
            elif choice == "4":
                report_menu(report_service)
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Invalid choice.")
    finally:
        db.close()


if __name__ == "__main__":
    main()