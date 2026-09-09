# Patient Record Manager

An educational Python and SQLite command-line project that demonstrates CRUD
operations, validation, and automated testing. It is **not** a healthcare
application and must not be used with real patient information.

## Safety and privacy

- The database is created outside the repository by default, at
  `~/.patient-record-manager/patients.db`.
- Database files, virtual environments, and environment files are ignored by
  Git. Never commit patient data.
- There is no authentication, multi-user access, encryption-at-rest guarantee,
  audit log, backup policy, or clinical validation. Those capabilities are
  required before any real-world healthcare use.

## Design

- `patient.py` validates domain values and review flags.
- `database.py` owns constrained SQLite persistence and safe update fields.
- `main.py` handles resilient command-line input.

The database validates names, ages, weights, ISO dates, and status values.
Only `status` and `discharge_date` can be updated through the data layer.

## Run

```bash
python main.py
```

## Test

From the repository root:

```bash
python -m pytest Patient-Record-Manager
```

