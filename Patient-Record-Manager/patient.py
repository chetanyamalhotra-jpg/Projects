def validate_patient_input(name, age, weight_kg):
    """
    Validates patient input before it's saved to the database.
    Raises ValueError with a clear message if invalid.
    """
    if not name or not name.strip():
        raise ValueError("Name cannot be empty.")

    if age is None or age < 0:
        raise ValueError("Age cannot be negative.")

    if age > 130:
        raise ValueError("Age seems unrealistic. Please check the value.")

    if weight_kg is None or weight_kg <= 0:
        raise ValueError("Weight must be a positive number.")

    if weight_kg > 500:
        raise ValueError("Weight seems unrealistic. Please check the value.")

    return True


def flag_patient(age, weight_kg):
    """
    Returns a review flag/note if the patient's age or weight
    falls outside typical expected ranges. Returns None if no flag needed.
    """
    flags = []

    if age >= 90:
        flags.append("Advanced age — consider closer monitoring")
    if age < 1:
        flags.append("Infant — verify age entered in correct units")
    if weight_kg < 3:
        flags.append("Very low weight — verify units (kg vs lb)")
    if weight_kg > 150:
        flags.append("Very high weight — verify entry")

    if flags:
        return "; ".join(flags)
    return None

if __name__ == "__main__":
    print(validate_patient_input("Test", 45, 70))  # prints True

    try:
        validate_patient_input("", 45, 70)
    except ValueError as e:
        print("Caught error:", e)

    print(flag_patient(95, 70))   # shows advanced age flag
    print(flag_patient(45, 70))   # prints None