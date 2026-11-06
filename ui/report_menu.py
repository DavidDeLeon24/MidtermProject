class ReportMenu:
    def __init__(self, service):
        self.service = service

    def run(self):
        while True:
            print("\n--- Reports ---")
            print("1. Available equipment")
            print("2. Outstanding loans")
            print("3. Most-borrowed equipment")
            print("4. Summary statistics")
            print("5. Members with outstanding loans")
            print("0. Back")
            choice = input("Choice: ").strip()
            
            if choice == "1":
                self.available()
            elif choice == "2":
                self.outstanding()
            elif choice == "3":
                self.most_borrowed()
            elif choice == "4":
                self.summary()
            elif choice == "5":
                self.members_with_loans()
            elif choice == "0":
                return
            else:
                print("  ! Invalid option.")

    def available(self):
        print("\nEquipment availability:")
        rows = self.service.available_equipment()
        if not rows:
            print("  (none)")
        else:
            for r in rows:
                print("  [" + str(r["id"]) + "] " + r["name"] + " (" + r["category"] + ") - available: " + str(r["available"]))

    def outstanding(self):
        print("\nOutstanding loans:")
        rows = self.service.outstanding_loans()
        if not rows:
            print("  (none)")
        else:
            for r in rows:
                print("  Loan #" + str(r[0]) + ": " + r[2] + " borrowed " + str(r[5]) + " x " + r[4] + " on " + r[6])

    def most_borrowed(self):
        print("\nTop borrowed equipment:")
        rows = self.service.most_borrowed_equipment()
        for r in rows:
            print("  " + r["name"] + " (" + r["category"] + ") - " + str(r["times_borrowed"]) + " units")

    def summary(self):
        data = self.service.summary()
        print("\n  Equipment items    : " + str(data["equipment"]))
        print("  Registered members : " + str(data["members"]))
        print("  Outstanding loans  : " + str(data["outstanding_loans"]))

    def members_with_loans(self):
        print("\nMembers with outstanding loans:")
        rows = self.service.members_with_outstanding_loans()
        if not rows:
            print("  (none)")
        else:
            for r in rows:
                print("  " + r[0] + " - " + r[1] + " (" + str(r[2]) + " open loan(s))")