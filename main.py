from db import Database
from services import EquipmentService, MemberService, LoanService, ReportService
from ui import EquipmentMenu, MemberMenu, LoanMenu, ReportMenu

def main():
    # Initialize Database
    db = Database()
    
    # Initialize Services
    eq_svc = EquipmentService(db)
    mem_svc = MemberService(db)
    loan_svc = LoanService(db, eq_svc, mem_svc)
    rep_svc = ReportService(db)
    
    # Initialize Menus
    eq_menu = EquipmentMenu(eq_svc)
    mem_menu = MemberMenu(mem_svc)
    loan_menu = LoanMenu(loan_svc, eq_svc)
    rep_menu = ReportMenu(rep_svc)

    while True:
        print("\n" + "=" * 45)
        print("  EQUIPMENT LENDING MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Equipment Management")
        print("2. Member Management")
        print("3. Lending & Returns")
        print("4. Reports & Statistics")
        print("0. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            eq_menu.run()
        elif choice == "2":
            mem_menu.run()
        elif choice == "3":
            loan_menu.run()
        elif choice == "4":
            rep_menu.run()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("  ! Invalid option.")
            
    # Close the database connection when the program ends
    db.close()

if __name__ == "__main__":
    main()