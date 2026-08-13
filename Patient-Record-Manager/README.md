# Patient Record Manager

A command-line patient record management system built in Python, backed by SQLite.
Built as a practice project to apply SQL, database design, input validation,
and automated testing in a healthcare-relevant context.

## Features

- **Add** new patient records (name, age, weight, gender, diagnosis, admission date)
- **View** all patients or look up a single patient by ID
- **Update** patient records (e.g., mark as discharged, add a discharge date)
- **Delete** patient records
- **Search** patients by diagnosis or status (partial match supported)
- **Input validation** — rejects invalid names, negative/unrealistic ages, and
  negative/unrealistic weights before anything reaches the database
- **Review flagging** — automatically flags patients for review based on
  age or weight falling outside typical expected ranges (e.g., very advanced
  age, very low weight), without blocking the record from being saved

## Tech Stack

- Python 3
- SQLite (via Python's built-in `sqlite3` module)
- pytest for automated testing

## Project Structure

```
patient-record-manager/
├── database.py       # SQLite connection and all CRUD/search operations
├── patient.py         # Input validation and review-flagging logic
├── main.py            # Command-line interface
├── test_database.py   # pytest test suite for the database layer
└── README.md
```

This structure separates concerns deliberately:
- `database.py` only knows about storing and retrieving data
- `patient.py` only knows about validating and flagging clinical input
- `main.py` only handles user interaction, calling into the other two

This separation is what makes the database layer independently testable
without needing to simulate user input.

## Database Schema

| Column          | Type    | Notes                                  |
|-----------------|---------|-----------------------------------------|
| id              | INTEGER | Primary key, auto-increment             |
| name            | TEXT    | Required                                |
| age             | INTEGER | Required                                |
| weight_kg       | REAL    | Required                                |
| gender          | TEXT    |                                          |
| diagnosis       | TEXT    |                                          |
| admission_date  | TEXT    | Defaults to today's date if not given   |
| discharge_date  | TEXT    | Nullable — set when a patient is discharged |
| status          | TEXT    | Defaults to `"admitted"`                |

## How to Run

```bash
python main.py
```

You'll see a menu with options to add, view, update, delete, and search
patient records. The database file (`patients.db`) is created automatically
on first run.

## How to Run Tests

```bash
pytest test_database.py -v
```

Tests run against a separate temporary test database (`test_patients.db`),
so your real patient data is never affected. The test database is created
fresh before each test and deleted afterward.

## Example Usage

```
1. Add patient
2. View all patients
3. View patient by ID
4. Update patient
5. Delete patient
6. Search
7. Quit
Choose an option (1-7): 1
Name: John Doe
Age: 45
Weight (kg): 72
Gender: M
Diagnosis: Fever
Patient added successfully.
```

## Limitations

- Command-line interface only — no graphical or web interface (yet)
- No authentication or user accounts
- No concurrent access handling (single-user, local use only)
- Review flagging uses simple, illustrative rules — not based on validated
  clinical thresholds, and not intended for real clinical decision-making

## Planned Improvements

- Wrap core operations in a FastAPI layer to expose them as a web API
- Add authentication for multi-user access
- Containerize with Docker for easier deployment
- Expand review-flagging logic with more clinically grounded rules

---

*This is an educational/portfolio project and is not intended for use in
real clinical or healthcare settings.*