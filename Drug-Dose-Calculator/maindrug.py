"""
Drug Dose Calculator v1.0
--------------------------
Educational project — NOT for real clinical use.
Calculates approximate weight-based doses for Paracetamol, Amoxicillin, and ORS.

Formulas used (simplified, for learning purposes):
- Paracetamol: 15 mg/kg per dose, max single dose 1000 mg, max 4000 mg/day
- Amoxicillin: 25 mg/kg/day divided into 3 doses, max single dose 500 mg
- ORS: 20 ml/kg for maintenance (simplified — real practice often uses
  Holliday-Segar method, which is a stretch goal for a future version)
"""

# Constants — named instead of "magic numbers" scattered in the code,
# so dosing values are easy to find and update in one place.
PARACETAMOL_MG_PER_KG = 15
PARACETAMOL_MAX_SINGLE_DOSE = 1000
PARACETAMOL_MAX_DAILY_DOSE = 4000

AMOXICILLIN_MG_PER_KG_PER_DAY = 25
AMOXICILLIN_DOSES_PER_DAY = 3
AMOXICILLIN_MAX_SINGLE_DOSE = 500

ORS_ML_PER_KG = 20


def calculate_dose(drug_name, weight_kg, age_years):
    """
    Calculates recommended dose for a given drug based on weight and age.
    Returns a dict with: drug, dose, unit, frequency, notes.
    """
    drug_name = drug_name.lower()

    if drug_name == "paracetamol":
        dose = weight_kg * PARACETAMOL_MG_PER_KG
        # Cap at the max single dose — a real safety consideration,
        # not just a coding exercise. Never silently exceed a known max.
        if dose > PARACETAMOL_MAX_SINGLE_DOSE:
            dose = PARACETAMOL_MAX_SINGLE_DOSE
        unit = "mg"
        frequency = "every 4-6 hours"
        notes = f"Maximum {PARACETAMOL_MAX_DAILY_DOSE} mg total per day"

    elif drug_name == "amoxicillin":
        daily_dose = weight_kg * AMOXICILLIN_MG_PER_KG_PER_DAY
        dose = daily_dose / AMOXICILLIN_DOSES_PER_DAY
        if dose > AMOXICILLIN_MAX_SINGLE_DOSE:
            dose = AMOXICILLIN_MAX_SINGLE_DOSE
        unit = "mg"
        frequency = f"{AMOXICILLIN_DOSES_PER_DAY} times per day"
        notes = f"Maximum single dose {AMOXICILLIN_MAX_SINGLE_DOSE} mg"

    elif drug_name == "ors":
        dose = weight_kg * ORS_ML_PER_KG
        unit = "ml"
        frequency = "per day (maintenance)"
        notes = "Simplified formula — real practice may use Holliday-Segar method"

    else:
        # Should not normally be reached since main() validates drug choice
        # before calling this function, but kept as a safe fallback.
        dose = None
        unit = None
        frequency = None
        notes = "Drug not found"

    return {
        "drug": drug_name,
        "dose": dose,
        "unit": unit,
        "frequency": frequency,
        "notes": notes,
    }


def get_valid_float(prompt, min_value=None, allow_zero=False):
    """
    Repeatedly asks the user for a number until a valid one is entered.
    Handles: non-numeric input, negative numbers, and zero (if not allowed).
    Keeping this as its own function avoids repeating the same
    validation loop for both age and weight.
    """
    while True:
        raw_value = input(prompt).strip()

        if raw_value == "":
            print("Input cannot be empty. Please try again.")
            continue

        try:
            value = float(raw_value)
        except ValueError:
            print("That doesn't look like a number. Please try again.")
            continue

        if value < 0:
            print("Value cannot be negative. Please try again.")
            continue

        if value == 0 and not allow_zero:
            print("Value cannot be zero. Please try again.")
            continue

        if min_value is not None and value < min_value:
            print(f"Value seems unrealistic (too low). Please try again.")
            continue

        return value


def get_drug_choice():
    """
    Asks the user to select a drug from the menu, re-prompting on
    invalid input instead of crashing or silently failing.
    """
    drug_choices = {"1": "paracetamol", "2": "amoxicillin", "3": "ors"}

    while True:
        print("\nSelect a drug:")
        print("1. Paracetamol")
        print("2. Amoxicillin")
        print("3. ORS")
        drug_choice = input("Enter choice (1-3): ").strip()

        if drug_choice in drug_choices:
            return drug_choices[drug_choice]

        print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    print("Welcome to Drug Dose Calculator")
    print("DISCLAIMER: This tool is for educational purposes only.")
    print("It is NOT a substitute for professional medical advice,")
    print("diagnosis, or treatment. Always consult a qualified")
    print("healthcare provider before administering any medication.")

    while True:
        patient_name = input("\nEnter patient name (or 'q' to quit): ").strip()
        if patient_name.lower() == "q":
            print("Thank you for using Drug Dose Calculator. Goodbye!")
            break

        if patient_name == "":
            print("Patient name cannot be empty. Please try again.")
            continue

        # Age can reasonably be very young (e.g. 0.1 for a newborn in months-as-years),
        # so we don't block small positive values, only zero/negative.
        age = get_valid_float("Enter patient age (years): ")

        # Weight has a sane minimum for a real patient — 1 kg guards against
        # obvious typos while still allowing low infant weights.
        weight = get_valid_float("Enter patient weight (kg): ", min_value=1)

        drug_name = get_drug_choice()
        result = calculate_dose(drug_name, weight, age)

        # Format dose nicely — avoid "270.0 mg" when "270 mg" reads better.
        dose_display = (
            int(result["dose"]) if result["dose"] == int(result["dose"])
            else round(result["dose"], 1)
        )

        print("PATIENT SUMMARY")
        print(f"Name:      {patient_name}")
        print(f"Age:       {age} years")
        print(f"Weight:    {weight} kg")
        print(f"Drug:      {result['drug'].capitalize()}")
        print(f"Dose:      {dose_display} {result['unit']}")
        print(f"Frequency: {result['frequency']}")
        print(f"Notes:     {result['notes']}")
        


if __name__ == "__main__":
    main()