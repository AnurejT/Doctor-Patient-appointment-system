# 🏥 MediBook — Doctor-Patient Appointment System

> A full-stack web application for managing doctor-patient appointments with role-based dashboards for Patients, Doctors, and Admins.

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightblue?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup & Run](#setup--run)
- [Roles & Workflows](#roles--workflows)
- [Screenshots](#screenshots)

---

## Overview

**MediBook** is a Flask-based web application that enables patients to register, browse approved doctors, and request appointments. Doctors can log in to manage incoming requests and confirmed appointments. An admin panel controls all registrations and approvals, ensuring only verified users access the system.

---

## ✨ Features

### 👤 Patient
- Register with name, phone, DOB, address, and password
- Login via phone number + password
- Browse all admin-approved doctors by specialization
- Send appointment requests to any approved doctor
- View confirmed appointments on a personal dashboard
- Update profile (name, DOB, address)

### 👨‍⚕️ Doctor
- Register with name, phone, DOB, specialization, and unique doctor ID
- Login via doctor ID + password
- View pending appointment requests with patient age & date
- Approve or reject appointment requests
- View & manage confirmed appointments
- Update profile details

### 🛡️ Admin
- Secure login with credentials
- Review and approve/reject patient registrations
- Review and approve/reject doctor registrations
- Delete any patient or doctor account
- View all approved patients and doctors in a tabbed dashboard

---

## 🛠 Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | Python 3.10, Flask 3.1.3            |
| ORM         | Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0 |
| Database    | SQLite (via `instance/forbooking.db`) |
| Frontend    | HTML5, Vanilla CSS (glassmorphism dark theme) |
| Fonts       | Google Fonts — Inter                |
| Icons       | Font Awesome 6.5                    |
| Templating  | Jinja2 (base template + blocks)     |

---

## 📁 Project Structure

```
Doctor-Patient-appointment-system/
│
├── app.py                  # Main Flask app & all routes
├── models.py               # SQLAlchemy models (Patient, Doctor, Appointment)
├── .gitignore              # Ignored files (venv, __pycache__, DB, etc.)
├── README.md               # This file
│
├── templates/
│   ├── base.html           # Shared layout (navbar, flash, design tokens)
│   ├── home.html           # Landing page with three portals
│   ├── regpat.html         # Patient registration form
│   ├── regdoc.html         # Doctor registration form
│   ├── logpat.html         # Patient login
│   ├── logdoc.html         # Doctor login
│   ├── logadmin.html       # Admin login
│   ├── patlogged.html      # Patient dashboard
│   ├── doclogged.html      # Doctor dashboard
│   ├── adminlogged.html    # Admin control panel (tabbed)
│   ├── update_pat.html     # Patient profile update
│   ├── update_doc.html     # Doctor profile update
│   └── contact.html        # Contact page
│
└── instance/
    └── forbooking.db       # SQLite database (auto-created, gitignored)
```

---

## 🚀 Setup & Run

### Prerequisites
- Python 3.10+ installed (via `py` launcher on Windows)

### 1. Clone the repository
```bash
git clone https://github.com/AnurejT/Doctor-Patient-appointment-system
cd Doctor-Patient-appointment-system
```

### 2. Create & activate virtual environment
```bash
# Windows
py -3.10 -m venv myvenv
.\myvenv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install flask flask_sqlalchemy
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5001
```

> The SQLite database (`instance/forbooking.db`) is created automatically on first run.

---

## 🔑 Admin Credentials

| Field    | Value    |
|----------|----------|
| Username | `anurej` |
| Password | `123`    |

> ⚠️ Change these in `app.py` before deploying to production.

---

## 🔄 Roles & Workflows

```
Patient registers → Admin approves → Patient logs in → Books appointment
                                                      ↓
Doctor registers → Admin approves → Doctor logs in → Approves/Rejects request
```

### Appointment Status Flow
```
PENDING → APPROVED (by doctor)
PENDING → REJECTED (by doctor)
APPROVED → REJECTED/DELETED (by doctor)
```

---

## 🗃️ Database Models

### Patient
| Column       | Type    | Notes              |
|--------------|---------|--------------------|
| id           | Integer | Primary key        |
| full_name    | String  |                    |
| phone_no     | String  | Unique, not null   |
| dob          | Date    |                    |
| address      | String  |                    |
| password     | String  |                    |
| is_approved  | Boolean | Default: False     |

### Doctor
| Column         | Type    | Notes            |
|----------------|---------|------------------|
| id             | Integer | Primary key      |
| full_name      | String  |                  |
| phone_no       | String  | Unique           |
| dob            | Date    |                  |
| address        | String  |                  |
| password       | String  |                  |
| doct_id        | String  | Unique doctor ID |
| specialization | String  |                  |
| is_approved    | Boolean | Default: False   |

### Appointment
| Column           | Type    | Notes                      |
|------------------|---------|----------------------------|
| id               | Integer | Primary key                |
| patient_id       | Integer | FK → Patient               |
| doctor_id        | Integer | FK → Doctor                |
| appointment_date | Date    |                            |
| status           | String  | pending / approved / rejected |

---

## 📸 Screenshots

> Live at `http://127.0.0.1:5001` after running locally.

| Page | Description |
|------|-------------|
| `/` | Landing page with patient, doctor, and admin portals |
| `/regpat` | Patient registration with two-column form |
| `/logpat` | Patient login |
| `/patlogged` | Patient dashboard with doctor radio-card selector |
| `/doclogged` | Doctor dashboard with pending/confirmed appointment panels |
| `/adminlogged` | Admin tabbed panel with approval queues and active user lists |

---

## 📌 Current Project Status

| Item | Status |
|------|--------|
| Patient registration & login | ✅ Complete |
| Doctor registration & login | ✅ Complete |
| Admin approval workflow | ✅ Complete |
| Appointment booking (patient) | ✅ Complete |
| Appointment management (doctor) | ✅ Complete |
| Profile update (patient & doctor) | ✅ Complete |
| Dark glassmorphism UI (all pages) | ✅ Complete |
| Shared base template (Jinja2) | ✅ Complete |
| SQLite database (auto-created) | ✅ Complete |
| `.gitignore` configured | ✅ Complete |
| Password hashing | ⏳ Planned |
| Email notifications | ⏳ Planned |
| Doctor availability calendar | ⏳ Planned |
| Production deployment (Gunicorn) | ⏳ Planned |

---

*Built with ❤️ using Flask & SQLite*
