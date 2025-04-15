from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String())
    phone_no = db.Column(db.String())
    dob = db.Column(db.Date)
    address = db.Column(db.String())
    password = db.Column(db.String())
    is_approved = db.Column(db.Boolean(), default = False)

class Doctor(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String())
    phone_no = db.Column(db.String())
    dob = db.Column(db.Date)
    address = db.Column(db.String())
    password = db.Column(db.String())
    doct_id = db.Column(db.String(), unique = True)
    specialization = db.Column(db.String())
    is_approved = db.Column(db.Boolean, default = False)

class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    date = db.Column(db.Date)

        
