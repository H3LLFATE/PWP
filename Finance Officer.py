

# ---------- FUNCTIONS ----------

def generate_bill():
    print("\n===== GENERATE BILL =====")

    patient_name = input("Enter patient name: ")

    # Validation for consultation fee
    while True:
        try:
            consultation_fee = float(input("Enter consultation fee (RM): "))
            if consultation_fee < 0:
                print("Fee cannot be negative.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter numbers only.")

    # Optional charges
    while True:
        try:
            additional_charges = float(input("Enter additional charges (RM): "))
            if additional_charges < 0:
                print("Charges cannot be negative.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter numbers only.")

    total = consultation_fee + additional_charges

    print("\n----- BILL -----")
    print(f"Patient Name       : {patient_name}")
    print(f"Consultation Fee   : RM {consultation_fee:.2f}")
    print(f"Additional Charges : RM {additional_charges:.2f}")
    print(f"TOTAL BILL         : RM {total:.2f}")

    # Save to file
    file = open("billing.txt", "a")

    file.write(
        patient_name + "|" +
        str(consultation_fee) + "|" +
        str(additional_charges) + "|" +
        str(total) + "\n"
    )

    file.close()

    print("Bill successfully saved.\n")


# -----------------------------------------------------

def make_payment():
    print("\n===== PAYMENT SECTION =====")

    patient_name = input("Enter patient name: ")

    while True:
        try:
            amount = float(input("Enter payment amount (RM): "))
            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                break
        except ValueError:
            print("Invalid amount.")

    print("\nPayment Methods:")
    print("1. Cash")
    print("2. Card")
    print("3. E-wallet")

    while True:
        method = input("Choose payment method: ")

        if method == "1":
            payment_method = "Cash"
            break
        elif method == "2":
            payment_method = "Card"
            break
        elif method == "3":
            payment_method = "E-wallet"
            break
        else:
            print("Invalid option.")

    # Save payment record
    file = open("payments.txt", "a")

    file.write(
        patient_name + "|" +
        str(amount) + "|" +
        payment_method + "\n"
    )

    file.close()

    print("\nPayment Recorded Successfully.")
    print(f"Patient : {patient_name}")
    print(f"Amount  : RM {amount:.2f}")
    print(f"Method  : {payment_method}\n")


# -----------------------------------------------------

def generate_report():
    print("\n===== FINANCIAL REPORT =====")

    total_revenue = 0

    try:
        file = open("payments.txt", "r")

        records = file.readlines()

        if len(records) == 0:
            print("No payment records found.\n")
        else:
            print("\n----- PAYMENT RECORDS -----")

            for line in records:
                data = line.strip().split("|")

                patient = data[0]
                amount = float(data[1])
                method = data[2]

                total_revenue += amount

                print(f"Patient : {patient}")
                print(f"Amount  : RM {amount:.2f}")
                print(f"Method  : {method}")
                print("---------------------------")

            print(f"\nTOTAL DAILY REVENUE : RM {total_revenue:.2f}\n")

        file.close()

    except FileNotFoundError:
        print("No payment file found.\n")


# -----------------------------------------------------

def finance_officer_menu():

    finance_officer_mode = True

    while finance_officer_mode:

        print("===================================")
        print("      FINANCE OFFICER MENU")
        print("===================================")
        print("1. Handle Billing")
        print("2. Make Payment")
        print("3. Generate Records")
        print("4. Exit")
        print("===================================")

        choice = input("Enter choice: ")

        if choice == "1":
            generate_bill()

        elif choice == "2":
            make_payment()

        elif choice == "3":
            generate_report()

        elif choice == "4":
            print("\nFinance Officer Mode Off.")
            print("Have a good day.\n")
            finance_officer_mode = False

        else:
            print("Invalid option. Please try again.\n")


# ---------- MAIN PROGRAM ----------

finance_officer_menu()
