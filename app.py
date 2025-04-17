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

@app.route('/')
def home():
    return render_template('home.html')    

@app.route('/regpat', methods = ['GET', 'POST'])
def reg_pat():
    if request.method == 'GET':
        return render_template('regpat.html')
    
    if request.method == 'POST':

        phone = request.form['phone']
        exist_patients = Patient.query.filter_by(phone_no = phone).all()

        if exist_patients:
            flash("Phone number already registered. Please log in or use a different number.")
            return redirect('/regpat')
        
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect('/regpat')
        
        dob_str = request.form['dob']
        dob_coverted = datetime.strptime(dob_str, '%Y-%m-%d').date()

        new_patient = Patient(
        full_name = request.form['full_name'],
        phone_no = phone,
        dob = dob_coverted,
        address = request.form['address'],
        password = confirm_password
        )
        
        db.session.add(new_patient)
        db.session.commit()
        return redirect('/')
    
@app.route('/regdoc', methods = ['GET', 'POST'])
def reg_doc():
    if request.method == 'GET':
        return render_template('regdoc.html')   
    
    if request.method == 'POST':

        phone = request.form['phone']
        exist_doctors_ph = Doctor.query.filter_by(phone_no = phone).all()

        if exist_doctors_ph:
            flash("Phone number already registered. Please log in or use a different number.")
            return redirect('/regdoc')
        
        doctor_id = request.form['doc_id']
        exist_doctors_docid = Doctor.query.filter_by(doct_id = doctor_id).all()

        if exist_doctors_docid:
            flash("This doctor ID already registered. Please log in or use a different doctor ID. ")
            return redirect('/regdoc')
        
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Passwords do not match. Please try again.")
            return redirect('/regdoc')

        dob_str = request.form['dob']
        dob_converted = datetime.strptime(dob_str, '%Y-%m-%d').date()

        new_doctor = Doctor(
        full_name = request.form['full_name'],
        phone_no = phone,
        dob = dob_converted,
        address = request.form['address'],
        password = password,
        specialization = request.form['speciality'],
        doct_id = request.form['doc_id']
        )

        db.session.add(new_doctor)
        db.session.commit()
        return redirect('/')   

@app.route('/logpat', methods = ['GET', 'POST'])
def log_pat():
    if request.method == 'GET':
        return render_template('logpat.html')

    if request.method == 'POST':
        
        phone = request.form['phone']
        password = request.form['password']

        patient = Patient.query.filter_by(phone_no = phone).first()

        if patient:

            if patient and patient.password == password:
                if patient.is_approved == True:
                    session['patient_id'] = patient.id
                    return redirect('/patlogged')
                else:
                    return 'Your account is not approved yet by the admin. Please wait for admin approval.'
            else:
                flash('Invalid password')
                return redirect('/logpat')
                
        else:
            return 'Invalid phone number'
        
@app.route('/patlogged')
def patient_logged():
    if 'patient_id' not in session:
        return redirect('/logpat')
    
    patient_id = session['patient_id']
    patients = Patient.query.filter_by(id = patient_id).all()
    approved_doctors = Doctor.query.filter_by(is_approved = True).all()
    fixed_appointments = Appointment.query.filter_by(status = 'approved').all()
    return render_template(
        'patlogged.html',
        patients = patients,
        approved_doctors = approved_doctors,
        fixed_appointments = fixed_appointments
    )

@app.route('/logdoc', methods = ['GET', 'POST'])
def log_doc():
    if request.method == 'GET':
        return render_template('logdoc.html') 

    if request.method == 'POST':

        doc_id = request.form['doctor_id']
        password = request.form['password']

        doctor = Doctor.query.filter_by(doct_id = doc_id).first()

        if doctor:

            if doctor and doctor.password == password:
                if doctor.is_approved == True:
                    session['doctor_id'] = doctor.id
                    return redirect('/doclogged')
                else:
                    return 'Your account is not approved yet by the admin. Please wait for admin approval.'
            else:
                flash('Invalid password')
                return redirect('/logdoc')
        
        else:
            flash('Invalid doctor ID')
            return redirect('/logdoc')      
        
@app.route('/doclogged')
def doctor_logged():
    if 'doctor_id' not in session:
        return redirect('/logdoc')
    
    doctor_id = session['doctor_id']
    doctors = Doctor.query.filter_by(id = doctor_id).all()
    appointment_requests = Appointment.query.filter_by(status = 'pending', doctor_id = doctor_id).all()
    fixed_appointments = Appointment.query.filter_by(status = 'approved', doctor_id = doctor_id).all()
    
    today = date.today()

    for appt in appointment_requests:
        if appt.patient:
            dob = appt.patient.dob
            appt.patient.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    for appt in fixed_appointments:
        if appt.patient:
            dob = appt.patient.dob
            appt.patient.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    return render_template('doclogged.html', doctors = doctors, appointment_requests = appointment_requests, fixed_appointments = fixed_appointments)
  
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
    patient_id = session.get('patient_id')
    doctor_id = request.form.get('doctor_id')
    appointment_date_str = request.form.get('appointment_date')

    appointment_date = datetime.strptime(appointment_date_str, '%Y-%m-%d').date()

    patient = Patient.query.get(patient_id)
    doctor = Doctor.query.get(doctor_id)

    if patient and doctor:
        exist_appointment_same_patient = Appointment.query.filter_by(doctor_id = doctor_id, patient_id = patient_id, appointment_date = appointment_date, status = 'pending').first()
        if exist_appointment_same_patient:
            flash(f"Doctor {doctor.full_name} has already got an appointment request on {appointment_date} from you. Try another date.")
            return redirect('/patlogged')
        
    if patient and doctor:
        exist_appointment = Appointment.query.filter_by(doctor_id = doctor_id, appointment_date = appointment_date, status = 'approved').first()
        if exist_appointment:
            flash(f"Doctor {doctor.full_name} has already an appointment on {appointment_date}. Try another date.")
            return redirect('/patlogged')
        
        appointment = Appointment(
        patient_id=patient.id,
        doctor_id=doctor.id,
        appointment_date=appointment_date,
        status='pending'  # ✅ This goes here
    )
    db.session.add(appointment)
    db.session.commit()
    flash(f"Appointment request sent to the doctor {doctor.full_name} for {appointment_date}.")
    return redirect('/patlogged')

@app.route('/approve_appointment/<int:appointment_id>', methods = ['POST'])
def approve_appointment(appointment_id):

    appointment = Appointment.query.get(appointment_id)
    if appointment.status == 'pending':
        appointment.status = 'approved'
        db.session.commit()
        flash("Appointment approved successfully.")
    return redirect('/doclogged')

@app.route('/reject_appointment/<int:appointment_id>', methods = ['POST'])
def reject_appointment(appointment_id):

    appointment = Appointment.query.get(appointment_id)
    if appointment and appointment.status in ['pending', 'approved']:
        appointment.status = 'rejected'
        db.session.commit()
        flash("Appointment rejected successfully.")
    return redirect('/doclogged') 

@app.route('/delete_appointment/<int:appointment_id>', methods = ['POST'])
def delete_appointment(appointment_id):

    appointment = Appointment.query.get(appointment_id)
    if appointment and appointment.status in ['pending', 'approved']:
        appointment.status = 'rejected'
        db.session.commit()
        flash("Appointment deleted successfully.")
    return redirect('/doclogged')     

@app.route('/contact_us')
def contact_us():
    return render_template('contact.html')

@app.route('/update_patient', methods=['GET', 'POST'])
def update_patient():
    patient_id = session.get('patient_id')
    patient = Patient.query.filter_by(id=patient_id).first()

    if not patient:
        flash("Patient not found.")
        return redirect('/patlogged')

    if request.method == 'POST':
        # Update patient data from form
        patient.full_name = request.form['full_name']
        patient.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        patient.address = request.form['address']

        db.session.commit()
        flash("Patient information updated successfully.")
        return redirect('/patlogged')  # Message shown on that page

    return render_template('update_pat.html', patient=patient)      

@app.route('/update_doctor', methods = ['GET', 'POST'])
def update_doctor():
    doctor_id = session.get('doctor_id')
    doctor = Doctor.query.filter_by(id = doctor_id).first()

    if not doctor:
        flash("Doctor not found.")
        return redirect('/doclogged')

    if request.method == 'POST':
        # Update doctor data from form
        doctor.full_name = request.form['full_name']
        doctor.phone_no = request.form['phone']
        doctor.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        doctor.address = request.form['address']
        doctor.specialization = request.form['speciality']

        db.session.commit()
        flash("Doctor information updated successfully.")
        return redirect('/doclogged')  # Message shown on that page
    
    return render_template('update_doc.html', doctor = doctor)
if __name__ == '__main__':
    app.run(debug=True, port=5001)
