from utils import ask_int, ask_non_empty, confirm

class EquipmentMenu:
    def __init__(self, service):
        self.service = service

    def run(self):
        while True:
            print("\n--- Equipment Management ---")
            print("1. Register equipment")
            print("2. Display all equipment")
            print("3. Search by name/category")
            print("4. Update equipment")
            print("5. Remove equipment")
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
            elif choice == "5":
                self.remove()
            elif choice == "0":
                return
            else:
                print("  ! Invalid option.")

    def register(self):
        name = ask_non_empty("Name: ")
        category = ask_non_empty("Category: ")
        qty = ask_int("Quantity available: ", minimum=0)
        try:
            new_id = self.service.add_equipment(name, category, qty)
            print("  Equipment registered with ID " + str(new_id))
        except ValueError as e:
            print("  ! Error: " + str(e))

    def display(self):
        items = self.service.list_equipment()
        if not items:
            print("  (no equipment registered)")
        else:
            for eq in items:
                avail = self.service.available_quantity(eq.equipment_id)
                print("  [" + str(eq.equipment_id) + "] " + eq.name + " (" + eq.category + ") - Total: " + str(eq.quantity) + " | Available: " + str(avail))

    def search(self):
        term = ask_non_empty("Search term: ")
        results = self.service.search_equipment(term)
        if not results:
            print("  (no matches)")
        else:
            for eq in results:
                avail = self.service.available_quantity(eq.equipment_id)
                print("  [" + str(eq.equipment_id) + "] " + eq.name + " (" + eq.category + ") - Available: " + str(avail))

    def update(self):
        eq_id = ask_int("Equipment ID to update: ")
        eq = self.service.get_equipment(eq_id)
        if eq is None:
            print("  ! Equipment not found.")
            return
            
        name = input("Name [" + eq.name + "]: ").strip()
        if not name:
            name = eq.name
            
        category = input("Category [" + eq.category + "]: ").strip()
        if not category:
            category = eq.category
            
        qty_raw = input("Total quantity [" + str(eq.quantity) + "]: ").strip()
        if not qty_raw:
            qty = eq.quantity
        else:
            qty = int(qty_raw)
            
        try:
            self.service.update_equipment(eq_id, name, category, qty)
            print("  Equipment updated.")
        except ValueError as e:
            print("  ! Error: " + str(e))

    def remove(self):
        eq_id = ask_int("Equipment ID to remove: ")
        eq = self.service.get_equipment(eq_id)
        if eq is None:
            print("  ! Equipment not found.")
            return
            
        if confirm("Delete " + eq.name + "? (y/n): "):
            try:
                self.service.remove_equipment(eq_id)
                print("  Equipment removed.")
            except ValueError as e:
                print("  ! Error: " + str(e))