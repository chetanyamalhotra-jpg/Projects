"""Command-line interface for the educational Patient Record Manager."""

from database import (
    add_patient,
    create_table,
    delete_patient,
    get_all_patients,
    get_patient_by_id,
    search_patients,
    update_patient,
)
from patient import flag_patient


def print_patient(row):
    """Format one record without exposing it outside the local CLI."""
    if row is None:
        print("Patient not found.")
        return
    print(
        f"ID: {row['id']} | Name: {row['name']} | Age: {row['age']} | "
        f"Weight: {row['weight_kg']}kg | Gender: {row['gender']} | "
        f"Diagnosis: {row['diagnosis']} | Admitted: {row['admission_date']} | "
        f"Discharged: {row['discharge_date']} | Status: {row['status']}"
    )


def prompt_patient_id(prompt):
    """Prompt until a positive integer ID is supplied, or allow cancellation."""
    while True:
        raw_value = input(f"{prompt} (blank to cancel): ").strip()
        if not raw_value:
            return None
        try:
            patient_id = int(raw_value)
        except ValueError:
            print("Patient ID must be a positive whole number.")
            continue
        if patient_id <= 0:
            print("Patient ID must be a positive whole number.")
            continue
        return patient_id


def add_patient_flow():
    """Collect and validate fields before storing them."""
    try:
        name = input("Name: ")
        age = int(input("Age: ").strip())
        weight_kg = float(input("Weight (kg): ").strip())
        gender = input("Gender: ")
        diagnosis = input("Diagnosis: ")
        patient_id = add_patient(name, age, weight_kg, gender, diagnosis)
    except ValueError as error:
        print(f"Error: {error}")
        return

    print(f"Patient {patient_id} added successfully.")
    flag = flag_patient(age, weight_kg)
    if flag:
        print(f"Review flag: {flag}")


def view_all_flow():
    """Display locally stored records."""
    patients = get_all_patients()
    if not patients:
        print("No patients found.")
    for patient in patients:
        print_patient(patient)


def view_one_flow():
    """Display one selected record."""
    patient_id = prompt_patient_id("Enter patient ID")
    if patient_id is not None:
        print_patient(get_patient_by_id(patient_id))


def update_flow():
    """Update a status and/or discharge date with central validation."""
    patient_id = prompt_patient_id("Enter patient ID to update")
    if patient_id is None or get_patient_by_id(patient_id) is None:
        if patient_id is not None:
            print("Patient not found.")
        return

    print("Leave a field blank to keep it unchanged.")
    status = input("New status (admitted/discharged): ").strip()
    discharge_date = input("Discharge date (YYYY-MM-DD): ").strip()
    fields = {}
    if status:
        fields["status"] = status
    if discharge_date:
        fields["discharge_date"] = discharge_date
    if not fields:
        print("No changes made.")
        return

    try:
        update_patient(patient_id, **fields)
    except ValueError as error:
        print(f"Error: {error}")
        return
    print("Patient updated.")


def delete_flow():
    """Delete one selected record."""
    patient_id = prompt_patient_id("Enter patient ID to delete")
    if patient_id is None:
        return
    if delete_patient(patient_id):
        print("Patient deleted.")
    else:
        print("Patient not found.")


def search_flow():
    """Search by diagnosis or status."""
    keyword = input("Search diagnosis/status: ").strip()
    if not keyword:
        print("Search term cannot be empty.")
        return
    for row in search_patients(keyword):
        print_patient(row)


def main():
    """Run the local-only command-line application."""
    create_table()
    print("Patient Record Manager — educational local-use project")
    print("Do not enter real patient information.")
    actions = {
        "1": add_patient_flow,
        "2": view_all_flow,
        "3": view_one_flow,
        "4": update_flow,
        "5": delete_flow,
        "6": search_flow,
    }
    while True:
        print(
            "\n1. Add patient\n2. View all\n3. View one\n4. Update\n"
            "5. Delete\n6. Search\n7. Quit"
        )
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Try again.")
        else:
            action()


if __name__ == "__main__":
    main()

