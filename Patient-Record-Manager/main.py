from database import create_table, add_patient, get_all_patients, get_patient_by_id, update_patient, delete_patient, search_patients
from patient import validate_patient_input, flag_patient


def print_patient(row):
    """Formats and prints a single patient row nicely."""
    if row is None:
        print("Patient not found.")
        return
    print(f"ID: {row[0]} | Name: {row[1]} | Age: {row[2]} | Weight: {row[3]}kg | "
          f"Gender: {row[4]} | Diagnosis: {row[5]} | Admitted: {row[6]} | "
          f"Discharged: {row[7]} | Status: {row[8]}")


def add_patient_flow():
    name = input("Name: ").strip()
    try:
        age = int(input("Age: "))
        weight_kg = float(input("Weight (kg): "))
        validate_patient_input(name, age, weight_kg)
    except ValueError as e:
        print("Error:", e)
        return

    gender = input("Gender: ").strip()
    diagnosis = input("Diagnosis: ").strip()

    add_patient(name, age, weight_kg, gender, diagnosis)
    print("Patient added successfully.")

    flag = flag_patient(age, weight_kg)
    if flag:
        print("⚠ Review flag:", flag)


def view_all_flow():
    patients = get_all_patients()
    if not patients:
        print("No patients found.")
    for p in patients:
        print_patient(p)


def view_one_flow():
    patient_id = int(input("Enter patient ID: "))
    print_patient(get_patient_by_id(patient_id))


def update_flow():
    patient_id = int(input("Enter patient ID to update: "))
    if get_patient_by_id(patient_id) is None:
        print("Patient not found.")
        return

    print("Leave blank to skip a field.")
    status = input("New status (e.g. discharged): ").strip()
    discharge_date = input("Discharge date (YYYY-MM-DD): ").strip()

    fields = {}
    if status:
        fields["status"] = status
    if discharge_date:
        fields["discharge_date"] = discharge_date

    if fields:
        update_patient(patient_id, **fields)
        print("Patient updated.")
    else:
        print("No changes made.")


def delete_flow():
    patient_id = int(input("Enter patient ID to delete: "))
    if delete_patient(patient_id):
        print("Patient deleted.")
    else:
        print("Patient not found.")


def search_flow():
    keyword = input("Search diagnosis/status: ").strip()
    results = search_patients(keyword)
    if not results:
        print("No matches found.")
    for r in results:
        print_patient(r)


def main():
    create_table()
    print("=" * 40)
    print("   Patient Record Manager")
    print("=" * 40)

    while True:
        print("\n1. Add patient")
        print("2. View all patients")
        print("3. View patient by ID")
        print("4. Update patient")
        print("5. Delete patient")
        print("6. Search")
        print("7. Quit")

        choice = input("Choose an option (1-7): ").strip()

        if choice == "1":
            add_patient_flow()
        elif choice == "2":
            view_all_flow()
        elif choice == "3":
            view_one_flow()
        elif choice == "4":
            update_flow()
        elif choice == "5":
            delete_flow()
        elif choice == "6":
            search_flow()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()