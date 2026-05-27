import os
from datetime import datetime

# ==========================================
# SYMBOLIC CONSTANTS
# ==========================================
MAX_APPOINTMENTS_PER_DAY = 10
DOCTORS_FILE = "doctors.txt"
APPOINTMENTS_FILE = "appointments.txt"


# ==========================================
# FILE INITIALIZATION HELPERS
# ==========================================
def initialize_files():
    """Ensures all necessary data text files exist for the admin module."""
    for file_name in [DOCTORS_FILE, APPOINTMENTS_FILE]:
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                pass


# ==========================================
# DATA LOADING AND SAVING FUNCTIONS
# ==========================================
def load_doctors():
    doctors = {}
    if os.path.exists(DOCTORS_FILE):
        with open(DOCTORS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        doc_id, name, spec, fee, slots_str = parts
                        slots = slots_str.split(",") if slots_str else []
                        doctors[doc_id] = {
                            "name": name,
                            "specialization": spec,
                            "fee": float(fee),
                            "slots": slots
                        }
    return doctors


def save_doctors(doctors):
    with open(DOCTORS_FILE, "w") as f:
        for doc_id, data in doctors.items():
            slots_str = ",".join(data["slots"])
            f.write(f"{doc_id}|{data['name']}|{data['specialization']}|{data['fee']}|{slots_str}\n")


def load_appointments():
    """Loaded as read-only for admin reporting purposes."""
    appointments = []
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 8:
                        appointments.append({
                            "app_id": parts[0],
                            "patient_id": parts[1],
                            "doctor_id": parts[2],
                            "date": parts[3],
                            "time_slot": parts[4],
                            "status": parts[5],
                            "diagnosis": parts[6],
                            "treatment": parts[7]
                        })
    return appointments


# ==========================================
# VALIDATION UTILITIES
# ==========================================
def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Invalid numerical input. Please enter a decimal value.")


# ==========================================
# ADMINISTRATOR MODULE
# ==========================================
def manage_doctors():
    while True:
        print("\n--- Manage Doctors ---")
        print("1. Add Doctor")
        print("2. Update Doctor")
        print("3. Remove Doctor")
        print("4. View All Doctors")
        print("0. Back to Admin Menu")

        choice = input("Enter choice: ").strip()
        doctors = load_doctors()

        if choice == "1":
            doc_id = input("Enter Doctor ID (e.g., DOC001): ").strip().upper()
            if doc_id in doctors:
                print("Error: Doctor ID already exists.")
                continue
            name = input("Enter Doctor Name: ").strip()
            spec = input("Enter Specialization: ").strip()
            fee = get_valid_float("Enter Consultation Fee ($): ")

            doctors[doc_id] = {
                "name": name,
                "specialization": spec,
                "fee": fee,
                "slots": ["09:00", "10:00", "11:00", "14:00", "15:00"]
            }
            save_doctors(doctors)
            print(f"Doctor {name} added successfully.")

        elif choice == "2":
            doc_id = input("Enter Doctor ID to update: ").strip().upper()
            if doc_id not in doctors:
                print("Error: Doctor not found.")
                continue
            print(f"Updating Dr. {doctors[doc_id]['name']}. Leave blank to keep current value.")
            name = input("Enter new Name: ").strip()
            spec = input("Enter new Specialization: ").strip()
            fee_str = input("Enter new Consultation Fee ($): ").strip()

            if name: doctors[doc_id]["name"] = name
            if spec: doctors[doc_id]["specialization"] = spec
            if fee_str:
                try:
                    doctors[doc_id]["fee"] = float(fee_str)
                except ValueError:
                    print("Invalid fee input. Keeping previous fee value.")

            save_doctors(doctors)
            print("Doctor profile updated successfully.")

        elif choice == "3":
            doc_id = input("Enter Doctor ID to remove: ").strip().upper()
            if doc_id in doctors:
                del doctors[doc_id]
                save_doctors(doctors)
                print("Doctor removed successfully.")
            else:
                print("Error: Doctor not found.")

        elif choice == "4":
            if not doctors:
                print("No doctors registered.")
            for d_id, info in doctors.items():
                print(
                    f"[{d_id}] Dr. {info['name']} | Spec: {info['specialization']} | Fee: ${info['fee']:.2f} | Slots: {', '.join(info['slots'])}")

        elif choice == "0":
            break
        else:
            print("Error: Invalid selection.")


def manage_clinic_schedule():
    doctors = load_doctors()
    if not doctors:
        print("Error: No doctors registered.")
        return

    doc_id = input("Enter Doctor ID: ").strip().upper()
    if doc_id not in doctors:
        print("Error: Doctor not found.")
        return

    print(f"Current slots for Dr. {doctors[doc_id]['name']}: {', '.join(doctors[doc_id]['slots'])}")
    slots_input = input("Enter new time slots separated by commas (e.g., 09:00,10:30,13:00): ").strip()

    if slots_input:
        new_slots = [s.strip() for s in slots_input.split(",") if s.strip()]
        doctors[doc_id]["slots"] = new_slots
        save_doctors(doctors)
        print("Clinic schedule updated successfully.")


def view_admin_reports():
    appointments = load_appointments()
    doctors = load_doctors()

    if not appointments:
        print("No historical appointment data found to generate metrics.")
        return

    print("\n================ CLINIC PERFORMANCE METRICS ================")
    date_counts = {}
    for app in appointments:
        date_counts[app["date"]] = date_counts.get(app["date"], 0) + 1
    print("\n--- Patient Load per Date ---")
    for date, count in sorted(date_counts.items()):
        print(f"Date: {date} | Total Appointments: {count}")

    doc_counts = {}
    for app in appointments:
        doc_counts[app["doctor_id"]] = doc_counts.get(app["doctor_id"], 0) + 1

    print("\n--- Doctor Ranking ---")
    if doc_counts:
        most_visited_id = max(doc_counts, key=doc_counts.get)
        doc_name = doctors.get(most_visited_id, {}).get("name", most_visited_id)
        print(f"Most Visited Doctor: Dr. {doc_name} ({doc_counts[most_visited_id]} appointments)")
    else:
        print("No calculation metrics available.")

    print("\n--- Capacity Utilization ---")
    total_possible_slots = len(doctors) * MAX_APPOINTMENTS_PER_DAY
    if total_possible_slots > 0:
        util_rate = (len(appointments) / total_possible_slots) * 100
        print(
            f"Utilization Rate: {util_rate:.2f}% (Cap limit: {MAX_APPOINTMENTS_PER_DAY} daily appointments per provider)")
    print("==========================================================")


def admin_menu():
    while True:
        print("\n--- Administrator Terminal ---")
        print("1. Manage Doctors")
        print("2. Configure Schedule Slots")
        print("3. View Reports")
        print("0. Exit Application")
        choice = input("Select operation: ").strip()
        if choice == "1":
            manage_doctors()
        elif choice == "2":
            manage_clinic_schedule()
        elif choice == "3":
            view_admin_reports()
        elif choice == "0":
            print("Exiting Administrator Terminal.")
            break
        else:
            print("Error: Invalid selection.")


if __name__ == "__main__":
    initialize_files()
    admin_menu()