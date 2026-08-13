"""
Tests for Patient Record Manager's database layer.
Run with: pytest test_database.py -v

IMPORTANT: These tests use a separate test database. This is done using pytest "fixtures" —
a way to set up and tear down test conditions automatically.
"""

import sqlite3
import os
import pytest
import database  # database.py file


TEST_DB = "test_patients.db"


@pytest.fixture
def test_db():
    """
    Sets up a fresh test database before each test, and deletes it after.
    This runs automatically for any test function that takes `test_db` as
    an argument, pytest handles the setup/teardown.
    """
    # Point database.py at the test database instead of the real one
    original_connect = database.create_connection
    database.create_connection = lambda: sqlite3.connect(TEST_DB)

    database.create_table()

    yield  # test runs here

    # Cleanup after the test finishes
    database.create_connection = original_connect
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_add_and_get_patient(test_db):
    database.add_patient("Alice", 30, 60.0, "F", "Fever", "2026-08-01")
    patients = database.get_all_patients()

    assert len(patients) == 1
    assert patients[0][1] == "Alice"  # name is column index 1
    assert patients[0][2] == 30       # age


def test_get_patient_by_id_found(test_db):
    database.add_patient("Bob", 45, 80.0, "M", "Cough", "2026-08-01")
    patient = database.get_patient_by_id(1)

    assert patient is not None
    assert patient[1] == "Bob"


def test_get_patient_by_id_not_found(test_db):
    patient = database.get_patient_by_id(999)
    assert patient is None


def test_update_patient(test_db):
    database.add_patient("Carol", 50, 65.0, "F", "Flu", "2026-08-01")
    updated = database.update_patient(1, status="discharged")

    assert updated is True
    patient = database.get_patient_by_id(1)
    assert patient[8] == "discharged"  # status is column index 8


def test_update_nonexistent_patient(test_db):
    updated = database.update_patient(999, status="discharged")
    assert updated is False


def test_delete_patient(test_db):
    database.add_patient("Dave", 60, 75.0, "M", "Injury", "2026-08-01")
    deleted = database.delete_patient(1)

    assert deleted is True
    assert database.get_patient_by_id(1) is None


def test_delete_nonexistent_patient(test_db):
    deleted = database.delete_patient(999)
    assert deleted is False


def test_search_patients_finds_match(test_db):
    database.add_patient("Eve", 35, 55.0, "F", "Fever", "2026-08-01")
    results = database.search_patients("fever")

    assert len(results) == 1
    assert results[0][1] == "Eve"


def test_search_patients_no_match(test_db):
    database.add_patient("Frank", 40, 70.0, "M", "Cold", "2026-08-01")
    results = database.search_patients("fever")

    assert len(results) == 0