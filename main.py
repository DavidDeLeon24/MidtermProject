"""
main.py
-------
Application entry-point for the Equipment Lending Management System.

Wires together:
  - Database connection   (db.database)
  - Service layer         (services.*)
  - Console UI            (ui.*)
"""
from db.database import Database
from services.equipment_service import EquipmentService
from services.member_service import MemberService
from services.loan_service import LoanService
from services.report_service import ReportService
from ui.equipment_menu import EquipmentMenu
from ui.member_menu import MemberMenu
from ui.loan_menu import LoanMenu
from ui.report_menu import ReportMenu


def main():
    db = Database()
    try:
        eq_svc = EquipmentService(db)
        mem_svc = MemberService(db)
        loan_svc = LoanService(db, eq_svc, mem_svc)
        rep_svc = ReportService(db)

        eq_menu = EquipmentMenu(eq_svc)
        mem_menu = MemberMenu(mem_svc)
        loan_menu = LoanMenu(loan_svc)
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
    finally:
        db.close()          # always close the connection


if __name__ == "__main__":
    main()