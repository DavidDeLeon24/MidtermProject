def ask_int(prompt, minimum=1):
    while True:
        raw = input(prompt).strip()
        if not raw:
            print("  ! Input cannot be empty.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print("  ! Please enter a valid integer.")
            continue
        if value < minimum:
            print("  ! Value must be at least " + str(minimum))
            continue
        return value

def ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  ! Field cannot be empty.")

def confirm(prompt="Are you sure? (y/n): "):
    answer = input(prompt).strip().lower()
    if answer == "y" or answer == "yes":
        return True
    return False