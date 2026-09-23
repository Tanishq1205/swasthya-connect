import sqlite3

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Drop tables to allow a clean reset
    cursor.execute('DROP TABLE IF EXISTS appointments')
    cursor.execute('DROP TABLE IF EXISTS feedback')
    cursor.execute('DROP TABLE IF EXISTS emergency_profile')
    cursor.execute('DROP TABLE IF EXISTS facilities')
    cursor.execute('DROP TABLE IF EXISTS users')

    # 1. Users Table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'citizen'
    )
    ''')

    # 2. Facilities Table (with Lat/Lon)
    cursor.execute('''
    CREATE TABLE facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        facility_type TEXT NOT NULL,
        area TEXT NOT NULL,
        contact TEXT NOT NULL,
        services TEXT NOT NULL,
        latitude REAL,
        longitude REAL
    )
    ''')

    # 3. Appointments Table
    cursor.execute('''
    CREATE TABLE appointments (
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

    # 4. Feedback Table
    cursor.execute('''
    CREATE TABLE feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comments TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 5. Emergency Profile Table
    cursor.execute('''
    CREATE TABLE emergency_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        emergency_contact_name TEXT,
        emergency_contact_phone TEXT,
        blood_group TEXT,
        allergies TEXT,
        medications TEXT,
        medical_conditions TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    # --- 18 Sample Facilities across Mumbai Suburbs ---
    sample_facilities = [
        # Chembur & Govandi
        ('Maa Hospital', 'Hospital', 'Chembur', '022-25220333', 'General Medicine, ICU, 24x7 Trauma, OPD', 19.0522, 72.8994),
        ('Chembur East Health Post', 'PHC', 'Chembur', '022-25281100', 'Immunization, Maternal Care, General OPD', 19.0601, 72.9015),
        ('Surana Sethia Multi-Specialty Hospital', 'Hospital', 'Chembur', '022-67868000', 'Cardiology, Orthopedics, Critical Care', 19.0558, 72.8931),
        ('Suburban Diagnostics Chembur', 'Diagnostic Center', 'Chembur', '022-61700000', 'Pathology, Digital X-Ray, ECG, Sonography', 19.0612, 72.8980),
        ('Shatabdi Municipal General Hospital', 'Hospital', 'Govandi', '022-25564070', 'Pediatrics, 24x7 Emergency, Gynecology', 19.0560, 72.9130),
        ('Govandi Maternity Home & Child Care', 'Clinic', 'Govandi', '022-25553210', 'Antenatal Checkups, Postnatal Care, Pediatrics', 19.0585, 72.9210),

        # Kurla & Ghatkopar
        ('KB Bhabha Municipal Hospital', 'Hospital', 'Kurla', '022-26500241', 'Orthopedics, Gynecology, 24x7 Casualty, ICU', 19.0688, 72.8790),
        ('Kurla Diagnostic & Imaging Centre', 'Diagnostic Center', 'Kurla', '022-25034455', 'CT Scan, Digital X-Ray, Blood Tests', 19.0720, 72.8812),
        ('Kurla West Urban Health Post', 'PHC', 'Kurla', '022-26521990', 'Vaccinations, Free Medicine Distribution, OPD', 19.0670, 72.8745),
        ('Rajawadi Municipal Hospital', 'Hospital', 'Ghatkopar', '022-25115066', 'Emergency Surgery, Burn Unit, ICU, Blood Bank', 19.0798, 72.9080),
        ('Ghatkopar East Health Post', 'PHC', 'Ghatkopar', '022-25123444', 'Family Planning, TB Treatment, General OPD', 19.0850, 72.9125),

        # Sion & Wadala
        ('Lokmanya Tilak Municipal General Hospital (Sion)', 'Hospital', 'Sion', '022-24076381', 'Level-1 Trauma Center, Cardiology, Neurology', 19.0434, 72.8634),
        ('Sion Community Health Post', 'PHC', 'Sion', '022-24018899', 'Pediatric Immunization, Routine Checkups', 19.0401, 72.8610),
        ('Wadala Municipal Dispensary', 'Clinic', 'Wadala', '022-24147722', 'General Medicine, Fever Clinic, Diabetes Screening', 19.0195, 72.8580),

        # Mankhurd & Vikhroli
        ('Mankhurd Urban Primary Health Centre', 'PHC', 'Mankhurd', '022-25586611', 'Primary Consultations, Maternal Welfare, Malnutrition Clinic', 19.0489, 72.9312),
        ('Godrej Memorial Hospital', 'Hospital', 'Vikhroli', '022-66417777', 'Multi-Specialty, Dialysis, Oncology, 24x7 Emergency', 19.0984, 72.9288),

        # Dadar & Bandra
        ('Dadar Municipal Dispensary', 'Clinic', 'Dadar', '022-24301122', 'Primary Care, Senior Citizen Consultations', 19.0178, 72.8478),
        ('B.J. Wadia Children Hospital', 'Hospital', 'Parel', '022-24197000', 'Super-Specialty Pediatric & Neonatal Care', 19.0035, 72.8415)
    ]

    cursor.executemany('''
    INSERT INTO facilities (name, facility_type, area, contact, services, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', sample_facilities)

    # Initial mock feedback review
    cursor.execute('''
    INSERT INTO feedback (user_name, rating, comments)
    VALUES ('Rahul Sharma', 5, 'Quick token confirmation and polite doctors at Chembur Health Post.')
    ''')

    conn.commit()
    conn.close()
    print("Database re-initialized successfully with 18 healthcare facilities.")

if __name__ == '__main__':
    init_db()