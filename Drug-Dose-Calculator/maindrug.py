"""Educational drug-dose arithmetic demonstration.

This application is not clinically validated and must never be used for real
prescribing, administration, or treatment decisions.
"""

from math import floor, isfinite

PARACETAMOL_MG_PER_KG = 15
PARACETAMOL_MAX_SINGLE_DOSE = 1000
PARACETAMOL_MAX_DAILY_DOSE = 4000
AMOXICILLIN_MG_PER_KG_PER_DAY = 25
AMOXICILLIN_DOSES_PER_DAY = 3
AMOXICILLIN_MAX_SINGLE_DOSE = 500
ORS_ML_PER_KG = 20


def _require_positive_finite(value, label):
    """Return a validated numeric value or raise ValueError."""
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a number.")
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be a number.") from error
    if not isfinite(number) or number <= 0:
        raise ValueError(f"{label} must be a finite number greater than zero.")
    return number


def calculate_dose(drug_name, weight_kg):
    """Return a bounded educational example for a supported drug.

    Age is intentionally not accepted because this simplified exercise does not
    implement age-specific rules. No administration schedule is generated.
    """
    weight_kg = _require_positive_finite(weight_kg, "Weight")
    drug_name = str(drug_name).strip().lower()

    if drug_name == "paracetamol":
        dose = min(weight_kg * PARACETAMOL_MG_PER_KG, PARACETAMOL_MAX_SINGLE_DOSE)
        max_doses_per_day = floor(PARACETAMOL_MAX_DAILY_DOSE / dose)
        return {
            "drug": drug_name,
            "dose": dose,
            "unit": "mg",
            "frequency": "No clinical schedule supplied",
            "max_doses_per_day": max_doses_per_day,
            "notes": (
                "Educational example only. This program does not determine an "
                "administration schedule. Its example daily cap is "
                f"{PARACETAMOL_MAX_DAILY_DOSE} mg."
            ),
        }

    if drug_name == "amoxicillin":
        dose = min(
            weight_kg * AMOXICILLIN_MG_PER_KG_PER_DAY / AMOXICILLIN_DOSES_PER_DAY,
            AMOXICILLIN_MAX_SINGLE_DOSE,
        )
        return {
            "drug": drug_name,
            "dose": dose,
            "unit": "mg",
            "frequency": "No clinical schedule supplied",
            "max_doses_per_day": None,
            "notes": "Educational example only; no clinical schedule is modeled.",
        }

    if drug_name == "ors":
        return {
            "drug": drug_name,
            "dose": weight_kg * ORS_ML_PER_KG,
            "unit": "ml",
            "frequency": "No clinical schedule supplied",
            "max_doses_per_day": None,
            "notes": "Educational example only; no clinical schedule is modeled.",
        }

    raise ValueError("Unsupported drug.")


def get_valid_float(prompt, min_value=None):
    """Prompt until a finite positive number satisfying an optional minimum."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = _require_positive_finite(raw_value, "Input")
        except ValueError as error:
            print(error)
            continue
        if min_value is not None and value < min_value:
            print("Value seems unrealistic (too low). Please try again.")
            continue
        return value


def get_drug_choice():
    """Prompt until a supported menu choice is selected."""
    choices = {"1": "paracetamol", "2": "amoxicillin", "3": "ors"}
    while True:
        print("\nSelect an educational example:")
        print("1. Paracetamol")
        print("2. Amoxicillin")
        print("3. ORS")
        choice = input("Enter choice (1-3): ").strip()
        if choice in choices:
            return choices[choice]
        print("Invalid choice. Please enter 1, 2, or 3.")


def format_amount(amount):
    """Format an amount without unnecessary decimal places."""
    return str(int(amount)) if amount.is_integer() else f"{amount:.1f}"


def main():
    print("Welcome to the Educational Drug Dose Calculator")
    print("This program is NOT for clinical use or real treatment decisions.")

    while True:
        patient_name = input(
            "\nEnter a fictional patient name (or 'q' to quit): "
        ).strip()
        if patient_name.lower() == "q":
            print("Goodbye!")
            return
        if not patient_name:
            print("Patient name cannot be empty.")
            continue

        age = get_valid_float("Enter patient age (years, display only): ")
        weight = get_valid_float("Enter patient weight (kg): ", min_value=1)
        result = calculate_dose(get_drug_choice(), weight)

        print("\nEDUCATIONAL EXAMPLE")
        print(f"Name: {patient_name}")
        print(f"Age: {format_amount(age)} years (not used for calculation)")
        print(f"Weight: {format_amount(weight)} kg")
        print(f"Example amount: {format_amount(result['dose'])} {result['unit']}")
        print(f"Schedule: {result['frequency']}")
        if result["max_doses_per_day"] is not None:
            print(f"Example maximum count in 24 hours: {result['max_doses_per_day']}")
        print(f"Notes: {result['notes']}")


if __name__ == "__main__":
    main()

