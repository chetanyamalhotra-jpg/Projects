"""Educational BMI calculator with validated input and testable pure functions."""

from math import isfinite


def require_positive_finite(value, label):
    """Convert a value to a finite positive float."""
    if isinstance(value, bool):
        raise ValueError(f"{label} must be a number.")
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{label} must be a number.") from error
    if not isfinite(number) or number <= 0:
        raise ValueError(f"{label} must be a finite number greater than zero.")
    return number


def calculate_bmi(weight_kg, height_m):
    """Calculate BMI from validated positive metric inputs."""
    weight_kg = require_positive_finite(weight_kg, "Weight")
    height_m = require_positive_finite(height_m, "Height")
    return weight_kg / height_m**2


def classify_bmi(bmi):
    """Return a display category for a validated BMI value."""
    bmi = require_positive_finite(bmi, "BMI")
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Healthy weight"
    if bmi < 30:
        return "Overweight"
    return "Obese"


def prompt_positive_float(prompt, label):
    """Prompt until a finite positive number is supplied."""
    while True:
        try:
            return require_positive_finite(input(prompt).strip(), label)
        except ValueError as error:
            print(error)


def main():
    """Run the educational command-line interface."""
    print("Welcome to the Educational Smart BMI Calculator")
    print("This result is informational only and is not medical advice.")
    name = input("Enter your name: ").strip() or "there"
    height_m = prompt_positive_float("Enter your height in metres: ", "Height")
    weight_kg = prompt_positive_float("Enter your weight in kg: ", "Weight")
    bmi = calculate_bmi(weight_kg, height_m)
    print(f"Hello {name}")
    print(f"Your BMI is: {bmi:.2f}")
    print(f"Category: {classify_bmi(bmi)}")


if __name__ == "__main__":
    main()

