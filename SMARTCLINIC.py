import os
from datetime import datetime

# ==========================================
# SYMBOLIC CONSTANTS
# ==========================================
MAX_APPOINTMENTS_PER_DAY = 10
PROFILES_FILE = "profile.txt"
PATIENTS_FILE = "patients.txt"
APPOINTMENTS_FILE = "appointments.txt"
BILLING_FILE = "billing.txt"


# ==========================================
# FILE INITIALIZATION HELPERS
# ==========================================
def initialize_files():
    """Ensures all necessary data text files exist. Adds default admin if no profiles."""
    for file_name in [PROFILES_FILE, PATIENTS_FILE, APPOINTMENTS_FILE, BILLING_FILE]:
        if not os.path.exists(file_name):
            with open(file_name, "w") as f:
                if file_name == PROFILES_FILE:
                    # Format: ID|ROLE|NAME|PASSWORD|SPEC|FEE|SLOTS
                    f.write("ADM001|ADMINISTRATOR|System Admin|admin123|||\n")


# ==========================================
# DATA LOADING AND SAVING FUNCTIONS
# ==========================================
def load_profiles():
    profiles = {}
    if os.path.exists(PROFILES_FILE):
        with open(PROFILES_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) >= 4:
                        u_id, role, name, password = parts[:4]
                        spec = parts[4] if len(parts) > 4 else ""
                        fee = float(parts[5]) if len(parts) > 5 and parts[5] else 0.0
                        slots_str = parts[6] if len(parts) > 6 else ""
                        slots = slots_str.split(",") if slots_str else []
                        profiles[u_id] = {
                            "role": role,
                            "name": name,
                            "password": password,
                            "specialization": spec,
                            "fee": fee,
                            "slots": slots
                        }
    return profiles


def save_profiles(profiles):
    with open(PROFILES_FILE, "w") as f:
        for u_id, data in profiles.items():
            slots_str = ",".join(data.get("slots", []))
            f.write(
                f"{u_id}|{data['role']}|{data['name']}|{data['password']}|{data.get('specialization', '')}|{data.get('fee', '')}|{slots_str}\n")


def get_doctors(profiles):
    """Filters profiles to return only doctors."""
    return {k: v for k, v in profiles.items() if v["role"] == "DOCTOR"}


def load_patients():
    patients = {}
    if os.path.exists(PATIENTS_FILE):
        with open(PATIENTS_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 5:
                        p_id, name, age, contact, info = parts
                        patients[p_id] = {
                            "name": name,
                            "age": int(age),
                            "contact": contact,
                            "info": info
                        }
    return patients


def save_patients(patients):
    with open(PATIENTS_FILE, "w") as f:
        for p_id, data in patients.items():
            f.write(f"{p_id}|{data['name']}|{data['age']}|{data['contact']}|{data['info']}\n")


def load_appointments():
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


def save_appointments(appointments):
    with open(APPOINTMENTS_FILE, "w") as f:
        for app in appointments:
            f.write(
                f"{app['app_id']}|{app['patient_id']}|{app['doctor_id']}|{app['date']}|{app['time_slot']}|{app['status']}|{app['diagnosis']}|{app['treatment']}\n")


def load_billing():
    billing = []
    if os.path.exists(BILLING_FILE):
        with open(BILLING_FILE, "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split("|")
                    if len(parts) == 9:
                        billing.append({
                            "bill_id": parts[0],
                            "app_id": parts[1],
                            "doctor_id": parts[2],
                            "date": parts[3],
                            "consult_fee": float(parts[4]),
                            "opt_charges": float(parts[5]),
                            "total": float(parts[6]),
                            "payment_method": parts[7],
                            "status": parts[8]
                        })
    return billing


def save_billing(billing):
    with open(BILLING_FILE, "w") as f:
        for b in billing:
            f.write(
                f"{b['bill_id']}|{b['app_id']}|{b['doctor_id']}|{b['date']}|{b['consult_fee']}|{b['opt_charges']}|{b['total']}|{b['payment_method']}|{b['status']}\n")


# ==========================================
# VALIDATION UTILITIES
# ==========================================
def get_valid_date(prompt):
    while True:
        date_str = input(prompt).strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")


def get_valid_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Error: Invalid numerical input. Please enter a decimal value.")


def get_valid_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Error: Invalid input. Please enter an integer.")


# ==========================================
# ADMINISTRATOR MODULE
# ==========================================
def manage_users():
    while True:
        print("\n--- Manage Users ---")
        print("1. Add User Profile")
        print("2. Update User Profile")
        print("3. Remove User Profile")
        print("4. View All Users")
        print("0. Back to Admin Menu")

        choice = input("Enter choice: ").strip()
        profiles = load_profiles()

        if choice == "1":
            u_id = input("Enter new User ID (e.g., DOC001, REC001): ").strip().upper()
            if u_id in profiles:
                print("Error: User ID already exists.")
                continue

            print("Select Role:\n1. ADMINISTRATOR\n2. DOCTOR\n3. RECEPTIONIST\n4. FINANCE OFFICER")
            role_map = {"1": "ADMINISTRATOR", "2": "DOCTOR", "3": "RECEPTIONIST", "4": "FINANCE OFFICER"}
            r_choice = input("Enter role option (1-4): ").strip()

            if r_choice not in role_map:
                print("Error: Invalid role selection.")
                continue
            role = role_map[r_choice]

            name = input("Enter Full Name: ").strip()
            password = input("Enter Login Password: ").strip()

            if role == "DOCTOR":
                spec = input("Enter Specialization: ").strip()
                fee = get_valid_float("Enter Consultation Fee ($): ")
                slots = ["09:00", "10:00", "11:00", "14:00", "15:00"]
            else:
                spec = ""
                fee = 0.0
                slots = []

            profiles[u_id] = {
                "role": role,
                "name": name,
                "password": password,
                "specialization": spec,
                "fee": fee,
                "slots": slots
            }
            save_profiles(profiles)
            print(f"{role.capitalize()} profile for {name} created successfully.")

        elif choice == "2":
            u_id = input("Enter User ID to update: ").strip().upper()
            if u_id not in profiles:
                print("Error: User not found.")
                continue

            user = profiles[u_id]
            print(f"Updating [{user['role']}] {user['name']}. Leave blank to keep current value.")
            name = input("Enter new Name: ").strip()
            password = input("Enter new Password: ").strip()

            if name: user["name"] = name
            if password: user["password"] = password

            if user["role"] == "DOCTOR":
                spec = input("Enter new Specialization: ").strip()
                fee_str = input("Enter new Consultation Fee ($): ").strip()
                if spec: user["specialization"] = spec
                if fee_str:
                    try:
                        user["fee"] = float(fee_str)
                    except ValueError:
                        print("Invalid fee input. Keeping previous fee value.")

            save_profiles(profiles)
            print("User profile updated successfully.")

        elif choice == "3":
            u_id = input("Enter User ID to remove: ").strip().upper()
            if u_id in profiles:
                del profiles[u_id]
                save_profiles(profiles)
                print("User removed successfully.")
            else:
                print("Error: User not found.")

        elif choice == "4":
            if not profiles:
                print("No users registered.")
            for uid, info in profiles.items():
                base_info = f"[{uid}] {info['role']} | Name: {info['name']}"
                if info['role'] == 'DOCTOR':
                    print(f"{base_info} | Spec: {info['specialization']} | Fee: ${info['fee']:.2f}")
                else:
                    print(base_info)

        elif choice == "0":
            break
        else:
            print("Error: Invalid selection.")


def manage_clinic_schedule():
    profiles = load_profiles()
    doctors = get_doctors(profiles)

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
        profiles[doc_id]["slots"] = new_slots
        save_profiles(profiles)
        print("Clinic schedule updated successfully.")


def view_admin_reports():
    appointments = load_appointments()
    profiles = load_profiles()
    doctors = get_doctors(profiles)

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
        print("1. Manage Users")
        print("2. Configure Schedule Slots")
        print("3. View Reports")
        print("0. Log Out")
        choice = input("Select operation: ").strip()
        if choice == "1":
            manage_users()
        elif choice == "2":
            manage_clinic_schedule()
        elif choice == "3":
            view_admin_reports()
        elif choice == "0":
            break
        else:
            print("Error: Invalid selection.")


# ==========================================
# RECEPTIONIST MODULE
# ==========================================
def register_patient():
    patients = load_patients()
    p_id = input("Enter Patient ID (e.g., PAT001): ").strip().upper()
    if p_id in patients:
        print("Error: Patient ID already matches an existing profile.")
        return

    name = input("Enter Full Name: ").strip()
    age = get_valid_int("Enter Age: ")
    contact = input("Enter Contact Number: ").strip()
    info = input("Enter Medical History / Allergies: ").strip()

    if not info:
        info = "None"

    patients[p_id] = {"name": name, "age": age, "contact": contact, "info": info}
    save_patients(patients)
    print(f"Patient [{p_id}] {name} registered successfully.")


def check_availability(doc_id, date, appointments, doctors):
    if doc_id not in doctors:
        return []

    booked_on_day = [app for app in appointments if
                     app["doctor_id"] == doc_id and app["date"] == date and app["status"] != "Cancelled"]
    if len(booked_on_day) >= MAX_APPOINTMENTS_PER_DAY:
        print("Warning: Doctor has reached daily capacity limit.")
        return []

    taken_slots = [app["time_slot"] for app in booked_on_day]
    available_slots = [slot for slot in doctors[doc_id]["slots"] if slot not in taken_slots]
    return available_slots


def manage_appointments():
    while True:
        print("\n--- Scheduling Menu ---")
        print("1. Book New Appointment")
        print("2. Cancel / Reschedule Booking")
        print("3. Check Availability Matrix")
        print("0. Return to Receptionist Menu")

        choice = input("Select operation: ").strip()
        appointments = load_appointments()
        profiles = load_profiles()
        doctors = get_doctors(profiles)
        patients = load_patients()

        if choice == "1":
            p_id = input("Enter Patient ID: ").strip().upper()
            if p_id not in patients:
                print("Error: Patient record not found.")
                continue

            doc_id = input("Enter Doctor ID: ").strip().upper()
            if doc_id not in doctors:
                print("Error: Doctor record not found.")
                continue

            date = get_valid_date("Enter Appointment Date (YYYY-MM-DD): ")
            open_slots = check_availability(doc_id, date, appointments, doctors)

            if not open_slots:
                print("Error: No available time slots on requested date.")
                continue

            print(f"Available slots for Dr. {doctors[doc_id]['name']}: {', '.join(open_slots)}")
            selected_slot = input("Enter preferred time slot: ").strip()

            if selected_slot not in open_slots:
                print("Error: Invalid time slot selection.")
                continue

            app_id = f"APP{len(appointments) + 101}"
            appointments.append({
                "app_id": app_id, "patient_id": p_id, "doctor_id": doc_id,
                "date": date, "time_slot": selected_slot, "status": "Booked",
                "diagnosis": "None", "treatment": "None"
            })
            save_appointments(appointments)
            print(f"Success: Appointment secured under Reference ID: [{app_id}].")

        elif choice == "2":
            app_id = input("Enter Appointment ID: ").strip().upper()
            target_app = next((a for a in appointments if a["app_id"] == app_id), None)

            if not target_app:
                print("Error: Appointment not found.")
                continue

            print(f"Record Found: {target_app['date']} @ {target_app['time_slot']} Status: [{target_app['status']}]")
            action = input("Type 'C' to Cancel, 'R' to Reschedule: ").strip().upper()

            if action == "C":
                target_app["status"] = "Cancelled"
                save_appointments(appointments)
                print("Booking status updated to Cancelled.")
            elif action == "R":
                new_date = get_valid_date("Enter New Date (YYYY-MM-DD): ")
                open_slots = check_availability(target_app["doctor_id"], new_date, appointments, doctors)
                if not open_slots:
                    print("Error: No open slots on that date.")
                    continue
                print(f"Available slots: {', '.join(open_slots)}")
                new_slot = input("Select time slot: ").strip()
                if new_slot in open_slots:
                    target_app["date"] = new_date
                    target_app["time_slot"] = new_slot
                    target_app["status"] = "Rescheduled"
                    save_appointments(appointments)
                    print("Booking adjusted successfully.")
                else:
                    print("Error: Invalid slot entry.")

        elif choice == "3":
            doc_id = input("Doctor ID: ").strip().upper()
            date = get_valid_date("Date (YYYY-MM-DD): ")
            slots = check_availability(doc_id, date, appointments, doctors)
            print(f"Open Time Windows: {', '.join(slots) if slots else 'NONE'}")

        elif choice == "0":
            break


def receptionist_menu():
    while True:
        print("\n--- Receptionist Menu ---")
        print("1. Register New Patient")
        print("2. Manage Appointments")
        print("0. Log Out")
        choice = input("Enter selection: ").strip()
        if choice == "1":
            register_patient()
        elif choice == "2":
            manage_appointments()
        elif choice == "0":
            break


# ==========================================
# DOCTOR MODULE
# ==========================================
def doctor_menu(doc_id):
    profiles = load_profiles()
    if doc_id not in profiles or profiles[doc_id]["role"] != "DOCTOR":
        print("Error: Profile verification failed.")
        return

    while True:
        print(f"\n--- Clinical Workspace: Dr. {profiles[doc_id]['name']} ---")
        print("1. View Daily Schedule")
        print("2. Add Consultation Notes & Treatment Plan")
        print("3. Modify Appointment Status Flag")
        print("4. View Patient Medical History")
        print("0. Log Out")

        choice = input("Enter option: ").strip()
        appointments = load_appointments()

        if choice == "1":
            target_date = get_valid_date("Enter date (YYYY-MM-DD): ")
            daily_list = [a for a in appointments if a["doctor_id"] == doc_id and a["date"] == target_date]

            print(f"\n--- Schedule Ledger [{target_date}] ---")
            if not daily_list:
                print("No client consultations scheduled on this day.")
            for app in sorted(daily_list, key=lambda x: x["time_slot"]):
                print(
                    f"Time: {app['time_slot']} | ID: {app['app_id']} | Patient ID: {app['patient_id']} | Status: {app['status']}")

        elif choice == "2":
            app_id = input("Enter Appointment ID: ").strip().upper()
            app = next((a for a in appointments if a["app_id"] == app_id and a["doctor_id"] == doc_id), None)

            if not app:
                print("Error: Consultation reference lookup failed.")
                continue

            diagnosis = input("Log Diagnostic Notes: ").strip()
            treatment = input("Prescribe Treatment / Medication: ").strip()

            app["diagnosis"] = diagnosis if diagnosis else "No anomalies detected"
            app["treatment"] = treatment if treatment else "Follow-up monitoring suggested"
            app["status"] = "Complete"

            save_appointments(appointments)
            print("Consultation notes successfully committed to patient records.")

        elif choice == "3":
            app_id = input("Enter Appointment ID: ").strip().upper()
            app = next((a for a in appointments if a["app_id"] == app_id and a["doctor_id"] == doc_id), None)
            if app:
                print("Select status entry alternative:")
                print("1. Complete\n2. Missed\n3. Cancelled")
                status_choice = input("Select choice: ").strip()
                if status_choice == "1":
                    app["status"] = "Complete"
                elif status_choice == "2":
                    app["status"] = "Missed"
                elif status_choice == "3":
                    app["status"] = "Cancelled"
                save_appointments(appointments)
                print("Appointment status modified.")
            else:
                print("Error: Record lookup missed.")

        elif choice == "4":
            patients = load_patients()
            p_id = input("Enter Patient ID (e.g., PAT001): ").strip().upper()

            if p_id not in patients:
                print("Error: Patient record not found in the system.")
                continue

            pat = patients[p_id]
            print(f"\n================ PATIENT PROFILE ================")
            print(f"Name: {pat['name']} | Age: {pat['age']} | Contact: {pat['contact']}")
            print(f"Medical History / Allergies: {pat['info']}")
            print("==================================================")

            # Fetch and display historical records for this specific patient
            pat_history = [a for a in appointments if a["patient_id"] == p_id]

            if not pat_history:
                print("No past appointment records found for this patient.")
            else:
                print("--- Consultation History ---")
                # Sort by date descending (newest appointments first)
                for app in sorted(pat_history, key=lambda x: x["date"], reverse=True):
                    # Attempt to fetch the attending doctor's name from profiles
                    doc_name = profiles.get(app["doctor_id"], {}).get("name", app["doctor_id"])

                    print(
                        f"\nDate: {app['date']} @ {app['time_slot']} | Ref: {app['app_id']} | Status: [{app['status']}]")
                    print(f"Attending Provider : Dr. {doc_name}")
                    print(f"Diagnosis          : {app['diagnosis']}")
                    print(f"Treatment          : {app['treatment']}")
            print("==================================================")

        elif choice == "0":
            break
        else:
            print("Error: Invalid selection.")


# ==========================================
# FINANCE OFFICER MODULE
# ==========================================
def finance_menu():
    while True:
        print("\n--- Financial Ledger Management ---")
        print("1. Generate Invoice Statement")
        print("2. Post Payment Settlement")
        print("3. View Revenue Reports")
        print("0. Log Out")

        choice = input("Execute structural choice: ").strip()
        billing = load_billing()
        appointments = load_appointments()
        profiles = load_profiles()
        doctors = get_doctors(profiles)

        if choice == "1":
            app_id = input("Verify Appointment ID for billing: ").strip().upper()
            app = next((a for a in appointments if a["app_id"] == app_id), None)

            if not app:
                print("Error: Booking record missing.")
                continue
            if app["status"] != "Complete":
                print("Warning: Consultation session must be marked 'Complete' by clinical staff first.")
                continue

            doc_fee = doctors.get(app["doctor_id"], {}).get("fee", 0.0)
            opt_charges = get_valid_float("Enter medication / prescription charges ($): ")
            total = doc_fee + opt_charges
            bill_id = f"INV{len(billing) + 1001}"

            billing.append({
                "bill_id": bill_id, "app_id": app_id, "doctor_id": app["doctor_id"],
                "date": app["date"], "consult_fee": doc_fee, "opt_charges": opt_charges,
                "total": total, "payment_method": "Unpaid", "status": "Outstanding"
            })
            save_billing(billing)
            print(
                f"Invoice [{bill_id}] drafted. Base Fee: ${doc_fee:.2f} + Add-ons: ${opt_charges:.2f} | Total: ${total:.2f}")

        elif choice == "2":
            bill_id = input("Enter Invoice ID: ").strip().upper()
            bill = next((b for b in billing if b["bill_id"] == bill_id), None)

            if not bill:
                print("Error: Statement reference index missing.")
                continue
            if bill["status"] == "Paid":
                print("Statement status matches cleared balance.")
                continue

            print(f"Open balance owing: ${bill['total']:.2f}")
            print("Select Method:\n1. Cash\n2. Card\n3. E-Wallet")
            pay_opt = input("Pick option: ").strip()

            method = "Cash"
            if pay_opt == "2":
                method = "Card"
            elif pay_opt == "3":
                method = "E-Wallet"

            bill["payment_method"] = method
            bill["status"] = "Paid"
            save_billing(billing)
            print(f"Receivables ledger updated. Balance cleared via payment mode: {method}.")

        elif choice == "3":
            print("\n============ REVENUE BALANCE SHEET ============")
            query_date = get_valid_date("Enter valuation date (YYYY-MM-DD): ")

            daily_rev = sum(b["total"] for b in billing if b["date"] == query_date and b["status"] == "Paid")
            print(f"Liquid Revenue Collection Total: ${daily_rev:.2f}")

            print("\n--- Yield Breakdown by Provider ---")
            doc_rev = {}
            for b in billing:
                if b["status"] == "Paid":
                    doc_rev[b["doctor_id"]] = doc_rev.get(b["doctor_id"], 0.0) + b["total"]
            for d_id, rev in doc_rev.items():
                name = doctors.get(d_id, {}).get("name", d_id)
                print(f"Dr. {name} ({d_id}) Revenue Generated: ${rev:.2f}")

            print("\n--- Outstanding Receivables ---")
            unpaid_bills = [b for b in billing if b["status"] == "Outstanding"]
            if not unpaid_bills:
                print("No outstanding liabilities reported.")
            for ub in unpaid_bills:
                print(f"Invoice ID: {ub['bill_id']} | Booking Ticket: {ub['app_id']} | Balance Due: ${ub['total']:.2f}")
            print("================================================")

        elif choice == "0":
            break


# ==========================================
# BANNER AND MAIN CONTROL ENGINE
# ==========================================
def banner():
    print("\n" + "=" * 60)
    print("SmartClinic - Clinic Appointment & Patient Management System")
    print("=" * 60)


def main():
    initialize_files()

    try:
        while True:
            attempts_left = 3

            while attempts_left > 0:
                banner()
                print("Please log in. (Default Admin -> ID: ADM001 | Password: admin123\n")

                # ----- COLLECTING ID -----
                while True:
                    user_id = input("Enter ID (or 'QUIT' to exit): ").strip().upper()
                    if user_id == "QUIT":
                        print("Shutting down SmartClinic engine. System Offline.")
                        return
                    if user_id == "":
                        print("ID is blank.")
                    else:
                        break

                # ----- COLLECTING PASSWORD -----
                while True:
                    password = input("Enter Password: ").strip()
                    if password == "":
                        print("Password is blank.")
                    else:
                        break

                profiles = load_profiles()

                if user_id in profiles and profiles[user_id]["password"] == password:
                    print("\nLogging In...")
                    role = profiles[user_id]["role"]

                    if role == "ADMINISTRATOR":
                        admin_menu()
                    elif role == "DOCTOR":
                        doctor_menu(user_id)
                    elif role == "RECEPTIONIST":
                        receptionist_menu()
                    elif role == "FINANCE OFFICER":
                        finance_menu()
                    else:
                        print(f"Invalid role '{role}' found in database records.")

                    # Break out of attempt loop on successful log out, returning to fresh banner login
                    break

                else:
                    attempts_left -= 1
                    print("\nEither ID or Password is incorrect.")
                    if attempts_left > 0:
                        print(f"{attempts_left} attempt(s) left.")
                    else:
                        print("No more attempts left. System locked for session.")
                        return

    except Exception as e:
        print(f"System Error: {e}")


if __name__ == "__main__":
    main()