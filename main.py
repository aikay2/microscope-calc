from database import create_table, insert_record, view_records, delete_record

# -----------------------------
# Microscope data
# -----------------------------
MICROSCOPE_TYPES = {
    1: ("Light Microscope", 40),
    2: ("Electron Microscope", 1000),
    3: ("SEM", 5000),
    4: ("TEM", 10000)
}

UNIT_TO_METERS = {
    "nm": 1e-9,
    "um": 1e-6,
    "mm": 1e-3,
    "cm": 1e-2,
    "m": 1
}

def convert_from_meters(value, unit):
    return value / UNIT_TO_METERS[unit]

# -----------------------------
# Input functions
# -----------------------------
def get_username():
    while True:
        username = input("Enter username: ").strip()
        if username:
            return username
        print("❌ Username cannot be empty.")

def get_measured_size():
    while True:
        try:
            value = float(input("Enter measured size: "))
            if value > 0:
                return value
            print("❌ Must be greater than 0.")
        except ValueError:
            print("❌ Invalid input.")

def select_microscope():
    print("\nSelect Microscope:")
    for k, (name, mag) in MICROSCOPE_TYPES.items():
        print(f"{k}. {name} ({mag}x)")

    while True:
        try:
            choice = int(input("Choice: "))
            if choice in MICROSCOPE_TYPES:
                return MICROSCOPE_TYPES[choice]
            print("❌ Invalid choice.")
        except ValueError:
            print("❌ Enter a number.")

def select_unit():
    units = list(UNIT_TO_METERS.keys())

    print("\nSelect Unit:")
    for i, u in enumerate(units, 1):
        print(f"{i}. {u}")

    while True:
        try:
            choice = int(input("Choice: "))
            if 1 <= choice <= len(units):
                return units[choice - 1]
            print("❌ Invalid choice.")
        except ValueError:
            print("❌ Enter a number.")

# -----------------------------
# Core calculation
# -----------------------------
def calculate():
    username = get_username()
    measured = get_measured_size()
    name, magnification = select_microscope()
    unit = select_unit()

    real_size = measured / magnification
    final_value = convert_from_meters(real_size, unit)

    print("\n📊 RESULT")
    print(f"User: {username}")
    print(f"Microscope: {name}")
    print(f"Real Size: {final_value} {unit}")

    # Save to DB
    insert_record(username, measured, real_size)
    print("✅ Saved to database.")

# -----------------------------
# View records
# -----------------------------
def show_records():
    records = view_records()

    if not records:
        print("📭 No records found.")
        return

    print("\n📚 Records:")
    for r in records:
        print(f"ID: {r[0]} | User: {r[1]} | Measured: {r[2]} | Real: {r[3]}")

# -----------------------------
# Delete record
# -----------------------------
def remove_record():
    show_records()

    try:
        record_id = int(input("Enter ID to delete: "))
        delete_record(record_id)
        print("🗑️ Record deleted.")
    except ValueError:
        print("❌ Invalid ID.")

# -----------------------------
# Menu
# -----------------------------
def menu():
    create_table()

    while True:
        print("\n==== MENU ====")
        print("1. New Calculation")
        print("2. View Records")
        print("3. Delete Record")
        print("4. Exit")

        choice = input("Select option: ")

        if choice == "1":
            calculate()
        elif choice == "2":
            show_records()
        elif choice == "3":
            remove_record()
        elif choice == "4":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")

# Run
if __name__ == "__main__":
    menu()
