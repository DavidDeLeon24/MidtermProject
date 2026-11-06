from utils import ask_non_empty

class MemberMenu:
    def __init__(self, service):
        self.service = service

    def run(self):
        while True:
            print("\n--- Member Management ---")
            print("1. Register member")
            print("2. Display all members")
            print("3. Search member by ID")
            print("4. Update member")
            print("0. Back")
            choice = input("Choice: ").strip()
            
            if choice == "1":
                self.register()
            elif choice == "2":
                self.display()
            elif choice == "3":
                self.search()
            elif choice == "4":
                self.update()
            elif choice == "0":
                return
            else:
                print("  ! Invalid option.")

    def register(self):
        mid = ask_non_empty("Member ID: ")
        name = ask_non_empty("Name: ")
        contact = ask_non_empty("Contact: ")
        try:
            self.service.register_member(mid, name, contact)
            print("  Member registered.")
        except ValueError as e:
            print("  ! Error: " + str(e))

    def display(self):
        items = self.service.list_members()
        if not items:
            print("  (no members registered)")
        else:
            for m in items:
                print("  " + m.member_id + ": " + m.name + " | " + m.contact)

    def search(self):
        mid = ask_non_empty("Member ID: ")
        m = self.service.get_member(mid)
        if m is None:
            print("  (not found)")
        else:
            print("  " + m.member_id + ": " + m.name + " | " + m.contact)

    def update(self):
        mid = ask_non_empty("Member ID to update: ")
        m = self.service.get_member(mid)
        if m is None:
            print("  ! Member not found.")
            return
            
        name = input("Name [" + m.name + "]: ").strip()
        if not name:
            name = m.name
            
        contact = input("Contact [" + m.contact + "]: ").strip()
        if not contact:
            contact = m.contact
            
        self.service.update_member(mid, name, contact)
        print("  Member updated.")