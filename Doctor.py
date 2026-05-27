
print("--- Doctor Menu ---")
doctor_username = input("Enter your username: ")
doctor_password = input("Enter your password: ")

# AUTHENTICATION
with open("doctor.txt", "r") as file:
    data = file.read().strip()

stored_user, stored_pass = data.split(",")

if doctor_username == stored_user and doctor_password == stored_pass:
    print("Login Successful")
    current_doctor_id = doctor_username

    # VIEW ASSIGNED APPOINTMENTS
    print("\n--- Your Appointments ---")
    with open("appointments.txt", "r") as file:
        for line in file:
            if current_doctor_id in line:
                print(line.strip())

    chosen_appointment_id = input("\nEnter chosen appointment ID: ")
    print("Select Action: 1. Record Consultation, 2. Update Status, 3. View Patient History")
    action = input("Enter action: ")

    if action == "1":
        # RECORD CONSULTATION
        diagnosis = input("Enter diagnosis: ")
        treatment = input("Enter treatment: ")
        with open("consultations.txt", "a") as file:
            file.write(f"{chosen_appointment_id},{diagnosis},{treatment}\n")
        print("Consultation recorded. Status: STATUS_DONE")
        print("Data sent to Finance")

    elif action == "2":
        # UPDATE STATUS
        print("Select Status: A. Absent, B. Present, C. Cancel")
        status_choice = input("Choice: ").upper()
        status = ""
        if status_choice == "A":
            status = "STATUS_ABSENT"
        elif status_choice == "B":
            status = "STATUS_PRESENT"
        elif status_choice == "C":
            status = "STATUS_CANCEL"

        print(f"Appointment {chosen_appointment_id} updated to {status}")
        print("Data sent to Finance")

    elif action == "3":
        # VIEW HISTORY
        patient_name = input("Enter Patient Name: ")
        print(f"\n--- History for {patient_name} ---")
        try:
            with open("patient_history.txt", "r") as file:
                for line in file:
                    if patient_name in line:
                        print(line.strip())
        except FileNotFoundError:
            print("No history file found")
else:
    print("Login Failed")