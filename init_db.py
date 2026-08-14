import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Module 1: Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'citizen'
    )
    ''')

    # Module 2: Facilities
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        facility_type TEXT NOT NULL,
        area TEXT NOT NULL,
        contact TEXT NOT NULL,
        services TEXT NOT NULL
    )
    ''')

    # Module 3: Appointments
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        facility_id INTEGER,
        patient_name TEXT NOT NULL,
        appointment_date TEXT NOT NULL,
        status TEXT DEFAULT 'Confirmed',
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (facility_id) REFERENCES facilities(id)
    )
    ''')

    # Module 4: Community Feedback
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comments TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Seed Sample Facilities
    cursor.execute('DELETE FROM facilities')
    sample_facilities = [
        ("Shatabdi Municipal Hospital", "Hospital", "Govandi", "022-25564070", "24x7 Emergency, OPD, Maternity"),
        ("Primary Health Center (PHC)", "PHC", "Chembur", "022-25221234", "Vaccination, Basic OPD, Maternal Care"),
        ("Arogya Community Clinic", "Clinic", "Kurla", "022-26509876", "General Medicine, Diabetes Care, Diagnostics"),
        ("LifeLine Diagnostic Center", "Diagnostic Center", "Ghatkopar", "022-25014321", "Blood Tests, ECG, Ultrasound, X-Ray")
    ]
    cursor.executemany('''
    INSERT INTO facilities (name, facility_type, area, contact, services)
    VALUES (?, ?, ?, ?, ?)
    ''', sample_facilities)

    conn.commit()
    conn.close()
    print("✓ SQLite database initialized and seeded with healthcare facilities.")

if __name__ == '__main__':
    init_db()