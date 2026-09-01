from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'swasthya_community_secret_key_2026'

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# ----------------- HOME ROUTE -----------------
@app.route('/')
def index():
    return render_template('index.html')

# ----------------- MODULE 1: AUTHENTICATION -----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db()
        try:
            conn.execute('INSERT INTO users (full_name, phone, password) VALUES (?, ?, ?)',
                         (full_name, phone, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Phone number already registered. Please log in.', 'danger')
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE phone = ? AND password = ?', (phone, password)).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['full_name']
            flash(f"Welcome, {user['full_name']}!", 'success')
            return redirect(url_for('directory'))
        else:
            flash('Invalid phone number or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

# ----------------- MODULE 2: HEALTHCARE DIRECTORY -----------------
@app.route('/directory')
def directory():
    search_query = request.args.get('search', '').strip()
    facility_type = request.args.get('type', '').strip()

    conn = get_db()
    query = "SELECT * FROM facilities WHERE 1=1"
    params = []

    if search_query:
        query += " AND (name LIKE ? OR area LIKE ?)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if facility_type and facility_type != 'All':
        query += " AND facility_type = ?"
        params.append(facility_type)

    facilities = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('directory.html', facilities=facilities, search_query=search_query, selected_type=facility_type)

# ----------------- MODULE 3: APPOINTMENT BOOKING -----------------
@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if 'user_id' not in session:
        flash('Please login to book appointments.', 'warning')
        return redirect(url_for('login'))

    conn = get_db()

    if request.method == 'POST':
        facility_id = request.form['facility_id']
        patient_name = request.form['patient_name']
        appointment_date = request.form['appointment_date']

        conn.execute('''
        INSERT INTO appointments (user_id, facility_id, patient_name, appointment_date)
        VALUES (?, ?, ?, ?)
        ''', (session['user_id'], facility_id, patient_name, appointment_date))
        conn.commit()
        flash('Appointment reserved successfully!', 'success')
        return redirect(url_for('appointments'))

    facilities = conn.execute('SELECT id, name FROM facilities').fetchall()
    user_appointments = conn.execute('''
        SELECT a.id, a.patient_name, a.appointment_date, a.status, f.name as facility_name
        FROM appointments a
        JOIN facilities f ON a.facility_id = f.id
        WHERE a.user_id = ?
        ORDER BY a.id DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()

    return render_template('appointments.html', facilities=facilities, appointments=user_appointments)

@app.route('/cancel-appointment/<int:id>', methods=['POST'])
def cancel_appointment(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    conn.execute('UPDATE appointments SET status = "Cancelled" WHERE id = ? AND user_id = ?', (id, session['user_id']))
    conn.commit()
    conn.close()
    flash('Appointment cancelled.', 'info')
    return redirect(url_for('appointments'))

# ----------------- MODULE 4: FEEDBACK & AWARENESS -----------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    conn = get_db()
    if request.method == 'POST':
        name = request.form.get('name', 'Citizen')
        rating = int(request.form.get('rating', 5))
        comments = request.form.get('comments', '')

        conn.execute('INSERT INTO feedback (user_name, rating, comments) VALUES (?, ?, ?)', (name, rating, comments))
        conn.commit()
        flash('Thank you! Your feedback will help improve local healthcare access.', 'success')
        return redirect(url_for('feedback'))

    all_feedback = conn.execute('SELECT * FROM feedback ORDER BY id DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('feedback.html', feedbacks=all_feedback)

# ----------------- EMERGENCY ASSIST ROUTES -----------------
@app.route('/emergency')
def emergency():
    user_profile = None
    if 'user_id' in session:
        conn = get_db()
        user_profile = conn.execute(
            'SELECT * FROM emergency_profiles WHERE user_id = ?', 
            (session['user_id'],)
        ).fetchone()
        conn.close()
    return render_template('emergency.html', profile=user_profile)

@app.route('/emergency-profile', methods=['GET', 'POST'])
def emergency_profile():
    if 'user_id' not in session:
        flash('Please log in to set up your Emergency Profile.', 'warning')
        return redirect(url_for('login'))

    conn = get_db()
    if request.method == 'POST':
        contact_name = request.form.get('emergency_contact_name', '').strip()
        contact_phone = request.form.get('emergency_contact_phone', '').strip()
        blood_group = request.form.get('blood_group', '').strip()
        allergies = request.form.get('allergies', '').strip()
        medications = request.form.get('medications', '').strip()
        medical_notes = request.form.get('medical_notes', '').strip()

        conn.execute('''
            INSERT INTO emergency_profiles (user_id, emergency_contact_name, emergency_contact_phone, blood_group, allergies, medications, medical_notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                emergency_contact_name=excluded.emergency_contact_name,
                emergency_contact_phone=excluded.emergency_contact_phone,
                blood_group=excluded.blood_group,
                allergies=excluded.allergies,
                medications=excluded.medications,
                medical_notes=excluded.medical_notes
        ''', (session['user_id'], contact_name, contact_phone, blood_group, allergies, medications, medical_notes))
        conn.commit()
        conn.close()
        flash('Emergency Profile updated successfully!', 'success')
        return redirect(url_for('emergency'))

    profile = conn.execute('SELECT * FROM emergency_profiles WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    return render_template('emergency_profile_edit.html', profile=profile)

if __name__ == '__main__':
    app.run(debug=True, port=5000)