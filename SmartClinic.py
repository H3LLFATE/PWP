import os
import time

# ==========================================
# SYMBOLIC CONSTANTS (File Paths)
# ==========================================
FILE_DOCTOR = "doctor.txt"
FILE_PATIENT = "patients.txt"
FILE_APPOINTMENT = "appointments.txt"
FILE_CONSULTATION = "consultations.txt"
FILE_BILLING = "billing.txt"
FILE_PAYMENT = "payments.txt"


# ==========================================
# UTILITY / HELPER FUNCTIONS
# ==========================================

def get_valid_input(prompt, is_numeric=False, is_float=False):
    """Handles basic input validation to prevent empty or invalid entries."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("Error: Input cannot be empty.")
            continue

        # Remove commas as we use comma-separated values (CSV) in txt files
        value = value.replace(",", "")

        if is_numeric:
            if value.isdigit():
                return value
            else:
                print("Invalid input. Please enter whole numbers only.")
        elif is_float:
            try:
                float(value)
                return value
            except ValueError:
                print("Invalid input. Please enter a valid amount (e.g., 50.00).")
        else:
            return value


def ensure_file_exists(filename):
    """Creates a blank file if it does not exist to avoid FileNotFoundError."""
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            pass


# ==========================================
# 1. ADMINISTRATOR
# ==========================================

def admin_menu():
    """Handles Administrator operations (Manage Doctors, View Reports)."""
    while True:
        print("\n" + "=" * 60)
        print("ADMINISTRATOR MENU")
        print("=" * 60)
        print("1. Register New Doctor")
        print("2. View All Doctors")
        print("3. View Clinic Reports")
        print("0. Return to Main Menu")
        print("=" * 60)

        choice = input("Enter choice: ")

        if choice == '1':
            register_doctor()
        elif choice == '2':
            view_doctors()
        elif choice == '3':
            admin_reports()
        elif choice == '0':
            break
        else:
            print("Invalid choice, please try again.")


def register_doctor():
    print("\n--- Register New Doctor ---")
    ensure_file_exists(FILE_DOCTOR)

    # Collect ID and check for duplicates
    while True:
        doc_id = get_valid_input("Enter Doctor's ID (eg: DOC001): ").upper()
        existing_ids = []
        with open(FILE_DOCTOR, "r") as f:
            for line in f:
                if line.strip():
                    existing_ids.append(line.split(",")[0])

        if doc_id in existing_ids:
            print("Error: Doctor ID already exists.")
        else:
            break

    name = get_valid_input("Enter Doctor's Name: ").upper()
    specialization = get_valid_input("Enter Specialization: ").upper()
    slots = get_valid_input("Enter Available Slots (eg: 10:00|11:00|14:00): ")
    fee = get_valid_input("Enter Consultation Fee (RM): ", is_float=True)

    with open(FILE_DOCTOR, "a") as f:
        f.write(f"{doc_id},{name},{specialization},{slots},{float(fee):.2f}\n")
    print(f"Success: Dr. {name} ({doc_id}) registered successfully.")


def view_doctors():
    print("\n--- Doctor Profiles ---")
    ensure_file_exists(FILE_DOCTOR)
    with open(FILE_DOCTOR, "r") as f:
        lines = f.readlines()
        if not lines:
            print("No doctors found.")
            return

        for line in lines:
            data = line.strip().split(",")
            if len(data) >= 5:
                print(f"ID: {data[0]} | Name: DR. {data[1]} | Spec: {data[2]} | Slots: {data[3]} | Fee: RM{data[4]}")


def admin_reports():
    print("\n--- System Reports ---")
    ensure_file_exists(FILE_APPOINTMENT)
    ensure_file_exists(FILE_PATIENT)

    with open(FILE_APPOINTMENT, "r") as f:
        appts = f.readlines()
    with open(FILE_PATIENT, "r") as f:
        patients = f.readlines()

    print(f"Total Registered Patients: {len(patients)}")
    print(f"Total Appointments Booked: {len(appts)}")

    # Calculate most visited doctor
    doc_counts = {}
    for appt in appts:
        data = appt.strip().split(",")
        if len(data) >= 3:
            doc_id = data[2]
            doc_counts[doc_id] = doc_counts.get(doc_id, 0) + 1

    if doc_counts:
        most_visited = max(doc_counts, key=doc_counts.get)
        print(f"Most Visited Doctor ID : {most_visited} ({doc_counts[most_visited]} appointments)")
    else:
        print("Most Visited Doctor    : N/A")


# ==========================================
# 2. RECEPTIONIST
# ==========================================

def receptionist_menu():
    while True:
        print("\n" + "=" * 60)
        print("RECEPTIONIST MENU")
        print("=" * 60)
        print("1. Register New Patient")
        print("2. Book Appointment")
        print("3. View All Appointments")
        print("0. Return to Main Menu")
        print("=" * 60)

        choice = input("Enter choice: ")

        if choice == '1':
            register_patient()
        elif choice == '2':
            book_appointment()
        elif choice == '3':
            view_appointments()
        elif choice == '0':
            break
        else:
            print("Invalid choice, please try again.")


def register_patient():
    print("\n--- Register New Patient ---")
    name = get_valid_input("Enter Patient Name: ").upper()
    contact = get_valid_input("Enter Contact Number: ", is_numeric=True)
    age = get_valid_input("Enter Age: ", is_numeric=True)

    ensure_file_exists(FILE_PATIENT)
    with open(FILE_PATIENT, "a") as file:
        file.write(f"{name},{contact},{age}\n")
    print(f"Success: Patient '{name}' registered.")


def book_appointment():
    ensure_file_exists(FILE_DOCTOR)
    ensure_file_exists(FILE_PATIENT)
    ensure_file_exists(FILE_APPOINTMENT)

    # 1. Verify Patient
    patient_name = get_valid_input("\nEnter Patient Name to book: ").upper()
    patient_found = False
    with open(FILE_PATIENT, "r") as file:
        for line in file:
            if patient_name == line.split(",")[0]:
                patient_found = True
                break

    if not patient_found:
        print(f"Error: '{patient_name}' is not registered. Please register them first.")
        return

    # 2. Show Doctors & Verify ID
    print("\n--- Available Doctors ---")
    valid_doctors = []
    doctor_slots = {}

    with open(FILE_DOCTOR, "r") as file:
        for line in file:
            if line.strip():
                data = line.strip().split(',')
                print(f"- ID: {data[0]} | Name: {data[1]} | Spec: {data[2]} | Slots: {data[3]}")
                valid_doctors.append(data[0])
                doctor_slots[data[0]] = data[3].split("|")

    if not valid_doctors:
        print("Error: No doctors in the system. Admin must add a doctor first.")
        return

    doc_id = get_valid_input("Enter Doctor ID from the list: ").upper()
    if doc_id not in valid_doctors:
        print(f"Error: Doctor '{doc_id}' does not exist.")
        return

    # 3. Schedule Time & Prevent Double Booking
    date = get_valid_input("Enter Date (DD-MM-YYYY): ")
    print(f"Available slots for {doc_id}: {', '.join(doctor_slots[doc_id])}")
    time_slot = get_valid_input("Enter Time Slot exactly as shown above: ")

    if time_slot not in doctor_slots[doc_id]:
        print("Error: Invalid time slot selected.")
        return

    # Double-booking check
    with open(FILE_APPOINTMENT, "r") as file:
        for line in file:
            data = line.strip().split(",")
            # Data format: ApptID, PatientName, DoctorID, Date, TimeSlot, Status
            if len(data) >= 6:
                if data[2] == doc_id and data[3] == date and data[4] == time_slot and data[5] != "CANCELLED":
                    print(f"Error: Dr. {doc_id} is already booked on {date} at {time_slot}.")
                    return

    # 4. Generate ID and Save
    appt_id = "APT" + str(int(time.time()))[-4:]
    with open(FILE_APPOINTMENT, "a") as file:
        file.write(f"{appt_id},{patient_name},{doc_id},{date},{time_slot},PENDING\n")

    print(f"Success: Appointment booked! Appointment ID is: {appt_id}")


def view_appointments():
    print("\n--- Current Appointments ---")
    ensure_file_exists(FILE_APPOINTMENT)
    with open(FILE_APPOINTMENT, "r") as file:
        content = file.readlines()
        if not content:
            print("No appointments found in the system.")
        else:
            for appt in content:
                data = appt.strip().split(",")
                if len(data) >= 6:
                    print(
                        f"[{data[5]}] ID: {data[0]} | Patient: {data[1]} | Dr: {data[2]} | Date: {data[3]} | Time: {data[4]}")


# ==========================================
# 3. DOCTOR
# ==========================================

def doctor_menu():
    ensure_file_exists(FILE_DOCTOR)

    print("\n--- Doctor Authentication ---")
    doc_id = get_valid_input("Enter your Doctor ID to login: ").upper()

    logged_in = False
    doc_name = ""
    with open(FILE_DOCTOR, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == doc_id:
                logged_in = True
                doc_name = data[1]
                doc_fee = data[4]
                break

    if not logged_in:
        print("Login Failed: Doctor ID not found.")
        return

    print(f"Welcome, DR. {doc_name}")

    while True:
        print("\n" + "=" * 60)
        print("DOCTOR MENU")
        print("=" * 60)
        print("1. View My Appointments")
        print("2. Record Consultation & Mark Complete")
        print("0. Logout")
        print("=" * 60)

        choice = input("Enter choice: ")

        if choice == '1':
            view_doc_appointments(doc_id)
        elif choice == '2':
            record_consultation(doc_id, doc_fee)
        elif choice == '0':
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def view_doc_appointments(doc_id):
    print(f"\n--- Appointments for DR. {doc_id} ---")
    ensure_file_exists(FILE_APPOINTMENT)
    found = False
    with open(FILE_APPOINTMENT, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if len(data) >= 6 and data[2] == doc_id:
                print(f"[{data[5]}] Appt ID: {data[0]} | Patient: {data[1]} | Date: {data[3]} | Time: {data[4]}")
                found = True
    if not found:
        print("No appointments assigned to you.")


def record_consultation(doc_id, base_fee):
    appt_id = get_valid_input("\nEnter chosen Appointment ID to record: ").upper()

    # Read appointments, find the match, update status
    ensure_file_exists(FILE_APPOINTMENT)
    with open(FILE_APPOINTMENT, "r") as file:
        appts = file.readlines()

    updated_appts = []
    appt_found = False
    patient_name = ""

    for appt in appts:
        data = appt.strip().split(",")
        if len(data) >= 6 and data[0] == appt_id and data[2] == doc_id:
            if data[5] == "COMPLETED":
                print("Error: Appointment is already marked completed.")
                return
            appt_found = True
            patient_name = data[1]
            data[5] = "COMPLETED"
            updated_appts.append(",".join(data) + "\n")
        else:
            updated_appts.append(appt)

    if not appt_found:
        print("Error: Appointment ID not found or does not belong to you.")
        return

    # Overwrite appointment file with updated status
    with open(FILE_APPOINTMENT, "w") as file:
        file.writelines(updated_appts)

    # Record the actual consultation
    diagnosis = get_valid_input("Enter Diagnosis: ")
    treatment = get_valid_input("Enter Prescribed Treatment: ")

    ensure_file_exists(FILE_CONSULTATION)
    with open(FILE_CONSULTATION, "a") as file:
        file.write(f"{appt_id},{patient_name},{doc_id},{diagnosis},{treatment},{base_fee}\n")

    print(f"Success: Consultation recorded for {patient_name}. Sent to Finance for billing.")


# ==========================================
# 4. FINANCE OFFICER MODULE
# ==========================================

def finance_menu():
    while True:
        print("\n" + "=" * 60)
        print("FINANCE OFFICER MENU")
        print("=" * 60)
        print("1. Generate Bill (from Consultation)")
        print("2. Record Payment")
        print("3. View Financial Report")
        print("0. Return to Main Menu")
        print("=" * 60)

        choice = input("Enter choice: ")

        if choice == '1':
            generate_bill()
        elif choice == '2':
            make_payment()
        elif choice == '3':
            generate_report()
        elif choice == '0':
            break
        else:
            print("Invalid choice, please try again.")


def generate_bill():
    print("\n===== GENERATE BILL =====")
    appt_id = get_valid_input("Enter Appointment ID to bill: ").upper()

    ensure_file_exists(FILE_CONSULTATION)
    ensure_file_exists(FILE_BILLING)

    # Check if already billed
    with open(FILE_BILLING, "r") as file:
        if appt_id in file.read():
            print("Error: This appointment has already been billed.")
            return

    # Find consultation data to pull base fee
    consultation_found = False
    with open(FILE_CONSULTATION, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[0] == appt_id:
                consultation_found = True
                patient_name = data[1]
                consultation_fee = float(data[5])
                break

    if not consultation_found:
        print("Error: No consultation record found for this Appointment ID.")
        return

    additional_charges = float(get_valid_input("Enter additional charges (RM) [e.g. Medicine]: ", is_float=True))
    total = consultation_fee + additional_charges

    print("\n----- INVOICE -----")
    print(f"Appt ID            : {appt_id}")
    print(f"Patient Name       : {patient_name}")
    print(f"Consultation Fee   : RM {consultation_fee:.2f}")
    print(f"Additional Charges : RM {additional_charges:.2f}")
    print(f"TOTAL BILL         : RM {total:.2f}")

    with open(FILE_BILLING, "a") as file:
        file.write(f"{appt_id},{patient_name},{consultation_fee:.2f},{additional_charges:.2f},{total:.2f}\n")
    print("Bill successfully saved.")


def make_payment():
    print("\n===== PAYMENT SECTION =====")
    patient_name = get_valid_input("Enter patient name: ").upper()
    amount = float(get_valid_input("Enter payment amount (RM): ", is_float=True))

    print("\nPayment Methods:")
    print("1. Cash")
    print("2. Card")
    print("3. E-wallet")

    while True:
        method_choice = input("Choose payment method (1-3): ")
        if method_choice == "1":
            method = "Cash"
            break
        elif method_choice == "2":
            method = "Card"
            break
        elif method_choice == "3":
            method = "E-wallet"
            break
        else:
            print("Invalid option.")

    ensure_file_exists(FILE_PAYMENT)
    with open(FILE_PAYMENT, "a") as file:
        file.write(f"{patient_name},{amount:.2f},{method}\n")

    print("\nPayment Recorded Successfully.")
    print(f"Patient : {patient_name}")
    print(f"Amount  : RM {amount:.2f}")
    print(f"Method  : {method}")


def generate_report():
    print("\n===== FINANCIAL REPORT =====")
    total_revenue = 0.0
    ensure_file_exists(FILE_PAYMENT)

    with open(FILE_PAYMENT, "r") as file:
        records = file.readlines()

    if not records:
        print("No payment records found.")
    else:
        print("\n----- PAYMENT RECORDS -----")
        for line in records:
            data = line.strip().split(",")
            if len(data) >= 3:
                patient = data[0]
                amount = float(data[1])
                method = data[2]
                total_revenue += amount
                print(f"Patient: {patient} | Amount: RM{amount:.2f} | Method: {method}")

        print("-" * 30)
        print(f"TOTAL CLINIC REVENUE : RM {total_revenue:.2f}")


# ==========================================
# MAIN MENU
# ==========================================

def main():
    while True:
        print("\n" + "=" * 60)
        print("SmartClinic - Appointment & Patient System")
        print("=" * 60)
        print("1. Administrator")
        print("2. Receptionist")
        print("3. Doctor")
        print("4. Finance Officer")
        print("0. Exit")
        print("=" * 60)

        choice = input("Enter your choice: ")

        if choice == '1':
            admin_menu()
        elif choice == '2':
            receptionist_menu()
        elif choice == '3':
            doctor_menu()
        elif choice == '4':
            finance_menu()
        elif choice == '0':
            print("Exiting SmartClinic System. Goodbye!")
            break
        else:
            print("Invalid entry. Please select a number from 0 to 4.")


if __name__ == "__main__":
    main()