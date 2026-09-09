"""SQLite persistence for the educational Patient Record Manager."""

import os
import sqlite3
from contextlib import closing
from datetime import date
from pathlib import Path

from patient import (
    validate_iso_date,
    validate_patient_id,
    validate_patient_input,
    validate_status,
    validate_text,
)

DEFAULT_DATABASE_PATH = Path.home() / ".patient-record-manager" / "patients.db"
_database_path = Path(
    os.environ.get("PATIENT_RECORD_DB", DEFAULT_DATABASE_PATH)
).expanduser()
EDITABLE_FIELDS = {"status", "discharge_date"}


def get_database_path():
    """Return the configured database path."""
    return _database_path


def set_database_path(path):
    """Set the database path, primarily for local tests."""
    global _database_path
    _database_path = Path(path).expanduser()


def create_connection():
    """Create a local SQLite connection outside the repository by default."""
    _database_path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    connection = sqlite3.connect(_database_path)
    connection.row_factory = sqlite3.Row
    try:
        os.chmod(_database_path, 0o600)
    except OSError:
        pass
    return connection


def create_table():
    """Create the constrained patients table when it does not yet exist."""
    with closing(create_connection()) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL CHECK(length(trim(name)) > 0),
                    age INTEGER NOT NULL CHECK(age BETWEEN 0 AND 130),
                    weight_kg REAL NOT NULL CHECK(weight_kg > 0 AND weight_kg <= 500),
                    gender TEXT,
                    diagnosis TEXT,
                    admission_date TEXT NOT NULL,
                    discharge_date TEXT,
                    status TEXT NOT NULL DEFAULT 'admitted'
                        CHECK(status IN ('admitted', 'discharged'))
                )
                """
            )


def add_patient(name, age, weight_kg, gender, diagnosis, admission_date=None):
    """Validate and insert a patient record."""
    name, age, weight_kg = validate_patient_input(name, age, weight_kg)
    gender = validate_text(gender, "Gender", max_length=40)
    diagnosis = validate_text(diagnosis, "Diagnosis", required=True, max_length=200)
    admission_date = validate_iso_date(
        admission_date or date.today().isoformat(), "Admission date"
    )
    with closing(create_connection()) as connection:
        with connection:
            cursor = connection.execute(
                """
                INSERT INTO patients
                    (name, age, weight_kg, gender, diagnosis, admission_date)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, age, weight_kg, gender, diagnosis, admission_date),
            )
            return cursor.lastrowid


def get_all_patients():
    """Return all records ordered by identifier."""
    with closing(create_connection()) as connection:
        return connection.execute("SELECT * FROM patients ORDER BY id").fetchall()


def get_patient_by_id(patient_id):
    """Return one record or None when it does not exist."""
    patient_id = validate_patient_id(patient_id)
    with closing(create_connection()) as connection:
        return connection.execute(
            "SELECT * FROM patients WHERE id = ?", (patient_id,)
        ).fetchone()


def update_patient(patient_id, **fields):
    """Safely update the explicitly supported fields on an existing record."""
    patient_id = validate_patient_id(patient_id)
    if not fields:
        return False
    unknown_fields = set(fields) - EDITABLE_FIELDS
    if unknown_fields:
        names = ", ".join(sorted(unknown_fields))
        raise ValueError(f"Unsupported update fields: {names}")

    cleaned_fields = {}
    if "status" in fields:
        cleaned_fields["status"] = validate_status(fields["status"])
    if "discharge_date" in fields:
        cleaned_fields["discharge_date"] = validate_iso_date(
            fields["discharge_date"], "Discharge date"
        )

    assignments = ", ".join(f"{field} = ?" for field in cleaned_fields)
    values = [*cleaned_fields.values(), patient_id]
    with closing(create_connection()) as connection:
        with connection:
            cursor = connection.execute(
                f"UPDATE patients SET {assignments} WHERE id = ?", values
            )
            return cursor.rowcount > 0


def delete_patient(patient_id):
    """Delete a record and report whether one was removed."""
    patient_id = validate_patient_id(patient_id)
    with closing(create_connection()) as connection:
        with connection:
            cursor = connection.execute(
                "DELETE FROM patients WHERE id = ?", (patient_id,)
            )
            return cursor.rowcount > 0


def search_patients(keyword):
    """Search diagnosis and status with a parameterized partial-match query."""
    keyword = validate_text(keyword, "Search term", required=True, max_length=200)
    pattern = f"%{keyword}%"
    with closing(create_connection()) as connection:
        return connection.execute(
            """
            SELECT * FROM patients
            WHERE diagnosis LIKE ? OR status LIKE ?
            ORDER BY id
            """,
            (pattern, pattern),
        ).fetchall()

