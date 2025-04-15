from flask import Flask, render_template, request, session, redirect, flash
from models import db, Patient, Doctor, Appointment
from datetime import datetime, date

ADMIN_USERNAME = 'anurej'
ADMIN_PASSWORD = '123'

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forbooking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/regpat', methods = ['GET', 'POST'])
def reg_pat():
    if request.method == 'GET':
        return render_template('regpat.html')
    
    if request.method == 'POST':
        
        dob_str = request.form['dob']
        dob_coverted = datetime.strptime(dob_str, '%Y-%m-%d').date()

        new_patient = Patient(
        full_name = request.form['full_name'],
        phone_no = request.form['phone'],
        dob = dob_coverted,
        address = request.form['address'],
        password = request.form['password']
        )
        
        db.session.add(new_patient)
        db.session.commit()
        return redirect('/')
    
@app.route('/regdoc', methods = ['GET', 'POST'])
def reg_doc():
    if request.method == 'GET':
        return render_template('regdoc.html')   
    
    if request.method == 'POST':

        dob_str = request.form['dob']
        dob_converted = datetime.strptime(dob_str, '%Y-%m-%d').date()

        new_doctor = Doctor(
        full_name = request.form['full_name'],
        phone_no = request.form['phone'],
        dob = dob_converted,
        address = request.form['address'],
        password = request.form['password'],
        specialization = request.form['speciality'],
        doct_id = request.form['doc_id']
        )

        db.session.add(new_doctor)
        db.session.commit()
        return redirect('/')   
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/logpat', methods = ['GET', 'POST'])
def log_pat():
    if request.method == 'GET':
        return render_template('logpat.html')

    if request.method == 'POST':
        
        phone = request.form['phone']
        password = request.form['password']

        patient = Patient.query.filter_by(phone_no = phone).first()

        if patient and patient.password == password:
            session['patient_id'] = patient.id
            return redirect('/patlogged')
        
        else:
            return 'Invalid phone number or password'
        
@app.route('/patlogged')
def patient_logged():
    if 'patient_id' not in session:
        return redirect('/logpat')
    
    patient_id = session['patient_id']
    approved_doctors = Doctor.query.filter_by(is_approved = True).all()
    appointments = Appointment.query.filter_by(patient_id = patient_id ).all()
    return render_template('patlogged.html', approved_doctors = approved_doctors, appointments = appointments)

@app.route('/logdoc', methods = ['GET', 'POST'])
def log_doc():
    if request.method == 'GET':
        return render_template('logdoc.html') 

    if request.method == 'POST':

        doc_id = request.form['doctor_id']
        password = request.form['password']

        doctor = Doctor.query.filter_by(doct_id = doc_id).first()

        if doctor and doctor.password == password:
            session['doctor_id'] = doctor.id
            return redirect('/doclogged')
        
        else:
            return 'Invalid doctor id or password'
        
@app.route('/doclogged')
def doctor_logged():
    if 'doctor_id' not in session:
        return redirect('/logdoc')
    
    return render_template('doclogged.html')

    
@app.route('/logadmin', methods = ['GET', 'POST'])
def log_admin():
    if request.method == 'GET':
        return render_template('logadmin.html')
    
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect('/adminlogged')
        
        else:
            return 'Invalid credentials for admin'
        
@app.route('/adminlogged')
def admin_logged():
    if not session.get('admin_logged_in'):
        return redirect('logadmin')

    pending_patients = Patient.query.filter_by(is_approved = False).all()
    approved_patients = Patient.query.filter_by(is_approved = True).all()

    pending_doctors = Doctor.query.filter_by(is_approved = False).all()
    approved_doctors = Doctor.query.filter_by(is_approved = True).all()

    return render_template('adminlogged.html', doctors = pending_doctors, approved_doctors = approved_doctors, patients = pending_patients, approved_patients = approved_patients) 

@app.route('/approve_patient/<int:patient_id>', methods=['POST'])
def approve_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        patient.is_approved = True
        db.session.commit()
        flash(f"Patient {patient.full_name} approved successfully.")
    return redirect('/adminlogged')

@app.route('/delete_patient/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if patient:
        db.session.delete(patient)
        db.session.commit()
        flash(f"Patient {patient.full_name} deleted successfully.")
    return redirect('/adminlogged')

@app.route('/approve_doctor/<int:doctor_id>', methods=['POST'])
def approve_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        doctor.is_approved = True
        db.session.commit()
        flash(f"Doctor {doctor.full_name} approved successfully.")
    return redirect('/adminlogged')

@app.route('/delete_doctor/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        db.session.delete(doctor)
        db.session.commit()
        flash(f"Doctor {doctor.full_name} deleted successfully.")
    return redirect('/adminlogged')

@app.route('/schedule_appointment', methods=['POST'])
def schedule_appointment():
    if request.method == 'POST':
        patient_id = session.get('patient_id')
        doctor_id = request.form['doctor_id']
        appointment_date_str = request.form['appointment_date']
        appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()

        patient = Patient.query.get(patient_id)
        doctor = Doctor.query.get(doctor_id)

        if patient and doctor:
            appointment = Appointment(
                patient_id=patient.id,
                doctor_id=doctor.id,
                appointment_date=appointment_date
            )
            db.session.add(appointment)
            db.session.commit()
            flash(f"Appointment scheduled with Dr. {doctor.full_name} on {appointment_date}.")
            return redirect('/patlogged')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
