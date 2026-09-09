from datetime import date

import database
import pytest


@pytest.fixture
def test_db(tmp_path):
    original_path = database.get_database_path()
    database.set_database_path(tmp_path / "test_patients.db")
    database.create_table()
    yield
    database.set_database_path(original_path)


def add_example_patient():
    return database.add_patient("Alice", 30, 60.0, "F", "Fever", "2026-08-01")


def test_add_and_get_patient(test_db):
    patient_id = add_example_patient()
    patient = database.get_patient_by_id(patient_id)

    assert patient["name"] == "Alice"
    assert patient["age"] == 30


def test_get_patient_by_id_not_found(test_db):
    assert database.get_patient_by_id(999) is None


def test_update_patient(test_db):
    patient_id = add_example_patient()

    assert database.update_patient(patient_id, status="discharged")
    assert database.get_patient_by_id(patient_id)["status"] == "discharged"


def test_update_rejects_unknown_field(test_db):
    patient_id = add_example_patient()

    with pytest.raises(ValueError, match="Unsupported update fields"):
        database.update_patient(patient_id, name="Unexpected")


def test_update_rejects_invalid_date(test_db):
    patient_id = add_example_patient()

    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        database.update_patient(patient_id, discharge_date="08/01/2026")


def test_delete_patient(test_db):
    patient_id = add_example_patient()

    assert database.delete_patient(patient_id)
    assert database.get_patient_by_id(patient_id) is None


def test_search_patients_finds_match(test_db):
    add_example_patient()

    results = database.search_patients("fever")

    assert len(results) == 1
    assert results[0]["name"] == "Alice"


@pytest.mark.parametrize("age, weight", [(-1, 60), (30, 0), (131, 60)])
def test_add_patient_rejects_invalid_core_values(test_db, age, weight):
    with pytest.raises(ValueError):
        database.add_patient(
            "Alice", age, weight, "F", "Fever", date.today().isoformat()
        )

