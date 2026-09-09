"""Validation helpers for the educational Patient Record Manager."""

from datetime import date
from math import isfinite

ALLOWED_STATUSES = {"admitted", "discharged"}


def validate_patient_input(name, age, weight_kg):
    """Validate core patient fields and return normalized values."""
    clean_name = validate_text(name, "Name", required=True, max_length=120)
    if isinstance(age, bool) or not isinstance(age, int):
        raise ValueError("Age must be a whole number.")
    if not 0 <= age <= 130:
        raise ValueError("Age must be between 0 and 130.")
    if isinstance(weight_kg, bool):
        raise ValueError("Weight must be a number.")
    try:
        clean_weight = float(weight_kg)
    except (TypeError, ValueError) as error:
        raise ValueError("Weight must be a number.") from error
    if not isfinite(clean_weight) or not 0 < clean_weight <= 500:
        raise ValueError("Weight must be a finite value between 0 and 500 kg.")
    return clean_name, age, clean_weight


def validate_text(value, field_name, required=False, max_length=200):
    """Normalize a short text value and enforce required/length constraints."""
    if value is None:
        value = ""
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be text.")
    clean_value = value.strip()
    if required and not clean_value:
        raise ValueError(f"{field_name} cannot be empty.")
    if len(clean_value) > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters.")
    return clean_value


def validate_iso_date(value, field_name):
    """Return a normalized ISO-8601 date or raise ValueError."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required in YYYY-MM-DD format.")
    try:
        return date.fromisoformat(value.strip()).isoformat()
    except ValueError as error:
        raise ValueError(f"{field_name} must use YYYY-MM-DD format.") from error


def validate_status(status):
    """Return a normalized, supported status."""
    clean_status = validate_text(status, "Status", required=True, max_length=20).lower()
    if clean_status not in ALLOWED_STATUSES:
        raise ValueError("Status must be 'admitted' or 'discharged'.")
    return clean_status


def validate_patient_id(patient_id):
    """Validate a positive integer record identifier."""
    if (
        isinstance(patient_id, bool)
        or not isinstance(patient_id, int)
        or patient_id <= 0
    ):
        raise ValueError("Patient ID must be a positive whole number.")
    return patient_id


def flag_patient(age, weight_kg):
    """Return an illustrative review flag for unusual entered values."""
    flags = []
    if age >= 90:
        flags.append("Advanced age — verify the entry")
    if age < 1:
        flags.append("Infant — verify age units")
    if weight_kg < 3:
        flags.append("Very low weight — verify units")
    if weight_kg > 150:
        flags.append("Very high weight — verify entry")
    return "; ".join(flags) if flags else None

