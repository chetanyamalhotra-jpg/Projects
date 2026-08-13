import sqlite3

def create_connection():
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect("patients.db")
    return conn

def create_table():
    """Creates the patients table if it doesn't already exist."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            weight_kg REAL NOT NULL,
            gender TEXT,
            diagnosis TEXT,
            admission_date TEXT,
            discharge_date TEXT,
            status TEXT DEFAULT 'admitted'
        )
    """)
    conn.commit()
    conn.close()

def add_patient(name, age, weight_kg, gender, diagnosis, admission_date=None):
    """Inserts a new patient record into the database."""
    conn = create_connection()
    cursor = conn.cursor()

    # If no admission_date is given, default to today's date
    if admission_date is None:
        from datetime import date
        admission_date = str(date.today())

    cursor.execute("""
        INSERT INTO patients (name, age, weight_kg, gender, diagnosis, admission_date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, weight_kg, gender, diagnosis, admission_date))

    conn.commit()
    conn.close()    

def get_all_patients():
    """Retrieves all patient records from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_patient_by_id(patient_id):
    """Retrieves a single patient record by ID. Returns None if not found."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_patient(patient_id, **fields):
    """
    Updates one or more fields for a given patient.
    Usage: update_patient(1, status="discharged", discharge_date="2026-08-12")
    """
    if not fields:
        return False  # nothing to update

    conn = create_connection()
    cursor = conn.cursor()

    # Build the SET clause dynamically, e.g. "status = ?, discharge_date = ?"
    set_clause = ", ".join(f"{key} = ?" for key in fields)
    values = list(fields.values())
    values.append(patient_id)  # for the WHERE clause

    cursor.execute(f"UPDATE patients SET {set_clause} WHERE id = ?", values)
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected > 0  # True if a row was actually updated


def delete_patient(patient_id):
    """Deletes a patient record by ID. Returns True if a row was deleted."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    return rows_affected > 0

def search_patients(keyword):
    """Searches patients by diagnosis or status matching the given keyword."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM patients
        WHERE diagnosis LIKE ? OR status LIKE ?
    """, (f"%{keyword}%", f"%{keyword}%"))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_table()
    results = search_patients("fever")
    for r in results:
        print(r)

    results2 = search_patients("discharged")
    for r in results2:
        print(r)