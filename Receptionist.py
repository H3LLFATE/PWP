import os
import time


def get_valid_input(prompt, is_numeric=False):
    while True:
        value = input(prompt).strip()
        if not value:
            print("Error: Input cannot be empty.")
            continue

        value = value.replace(",", "")

        if is_numeric:
            if value.isdigit():
                return value
            else:
                print("Invalid input. Please enter numbers only.")
        else:
            return value


def register_patient():
    print("\n--- Register New Patient ---")
    name = get_valid_input("Enter Patient Name: ")
    contact = get_valid_input("Enter Contact Number: ", is_numeric=True)
    age = get_valid_input("Enter Age: ", is_numeric=True)

    with open("patients.txt", "a") as file:
        file.write(f"{name},{contact},{age}\n")
    print(f"Success: Patient '{name}' registered.")


def book_appointment():
    if not os.path.exists("doctor.txt"):
        print("\nError: 'doctor.txt' not found. Please ask Admin to create doctor login.")
        return

    print("\n--- Available Doctors ---")
    valid_doctors = []

    with open("doctor.txt", "r") as file:
        data = file.read().strip()
        if data:
            doc_name = data.split(',')[0]
            print(f"- {doc_name}")
            valid_doctors.append(doc_name)

    patient_name = get_valid_input("\nEnter Patient Name to book: ")

    patient_found = False
    if os.path.exists("patients.txt"):
        with open("patients.txt", "r") as file:
            if patient_name in file.read():
                patient_found = True

    if not patient_found:
        print(f"Error: '{patient_name}' is not registered. Please register them first.")
        return

    doctors_id = get_valid_input("Enter Doctor Name/ID from the list: ")
    if doctors_id not in valid_doctors:
        print(f"Error: Doctor '{doctors_id}' does not exist in our records.")
        return

    date = get_valid_input("Enter Date (DD-MM-YYYY): ")

    appt_id = str(int(time.time()))[-4:]

    with open("appointments.txt", "a") as file:
        file.write(f"{appt_id},{patient_name},{doctors_id},{date},STATUS_PENDING\n")

    print(f"Success: Appointment booked! Appointment ID is: {appt_id}")


def view_appointments():
    print("\n--- Current Appointments ---")
    if not os.path.exists("appointments.txt"):
        print("No appointments found in the system.")
        return

    with open("appointments.txt", "r") as file:
        content = file.readlines()
        if not content:
            print("The appointment list is currently empty.")
        else:
            for appt in content:
                print(appt.strip())


def receptionist_menu():
    while True:
        print("\n--- Receptionist Management System ---")
        print("1. Register New Patient")
        print("2. Book Appointment")
        print("3. View All Appointments")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            register_patient()
        elif choice == '2':
            book_appointment()
        elif choice == '3':
            view_appointments()
        elif choice == '4':
            print("Exiting Receptionist Module...")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    receptionist_menu()