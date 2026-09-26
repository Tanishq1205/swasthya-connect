# 🩺 Swasthya Connect — Accessible Community Healthcare Portal

A trilingual (English, हिन्दी, मराठी), responsive public healthcare platform built to connect local citizens with municipal hospitals, primary health centers (PHCs), diagnostic labs, and emergency triage services.

## Live Demo & Deployment

[![Vercel Deployment](https://img.shields.io/badge/Deployed%20with-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://swasthya-connect-henna.vercel.app)

* **Production URL:** [https://swasthya-connect-henna.vercel.app](https://swasthya-connect-henna.vercel.app)
* **Hosting Platform:** Vercel (Serverless Python Runtime)
* **CI/CD:** Automatic builds triggered on push to `main`

### Deployment Details

* **Entry Point:** Handled via `/api/index.py` exposing the Flask WSGI application instance.
* **Routing Configuration (`vercel.json`):**
  ```json
  {
    "rewrites": [
      {
        "source": "/(.*)",
        "destination": "/api/index.py"
      }
    ]
  }

---

## 📌 Project Overview

Accessing municipal healthcare in densely populated urban and suburban areas is often hindered by long queues, scattered information, and language barriers. **Swasthya Connect** streamlines citizen access to primary and secondary healthcare through a unified, mobile-friendly interface designed with an MVC architectural approach.

---

## ✨ Key Features

* **📍 Proximity-Sorted Healthcare Directory:** Uses the browser's HTML5 Geolocation API alongside the **Haversine formula** on the backend to dynamically calculate distances and sort facilities from nearest to farthest.
* **🚨 Dedicated Emergency Mode (SOS):** High-contrast triage interface providing one-tap emergency calling (108 Ambulance, Police) and a personal emergency profile card (blood group, allergies, medications, emergency contacts).
* **🌐 Instant Trilingual Localization:** Seamless client-side switching between **English**, **हिन्दी**, and **मराठी** using `data-key` DOM attributes and `localStorage` persistence without requiring page reloads.
* **📅 OPD Consultation Scheduling:** Token booking gateway that links authenticated citizens with specific facilities via relational SQL foreign keys.
* **💡 Public Health Guides & Community Feedback:** Informational modules covering government initiatives (Ayushman Bharat, PMJAY) paired with a 5-star citizen review system.
* **🔐 Authentication & Session Security:** Session cookie encryption via Flask secret keys, parameterized SQL statements to eliminate SQL Injection, and input sanitation.

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | Python 3 / Flask | Application routing, business logic, session handling, request parsing |
| **Database** | SQLite3 (`database.db`) | ACID-compliant relational persistence with normalized tables and foreign keys |
| **Frontend Templates** | Jinja2 | Template inheritance (`base.html`), control flow, and dynamic data rendering |
| **Styling** | Tailwind CSS (CDN) | Modern utility-first, responsive UI and glassmorphism components |
| **Client Scripting** | Vanilla JavaScript (ES6+) | Geolocation detection, DOM manipulation, and dynamic language toggling |
| **WSGI Server** | Gunicorn | Production-grade WSGI server running on cloud infrastructure |
| **Deployment** | Render Cloud Platform | Continuous deployment synced with GitHub |

---

## 🗄️ Database Architecture

The relational schema consists of 5 normalized tables:

1. **`users`**: Manages citizen credentials (`id`, `full_name`, `phone` [UNIQUE], `password`, `role`).
2. **`facilities`**: Directory records (`id`, `name`, `facility_type`, `area`, `contact`, `services`, `latitude`, `longitude`).
3. **`appointments`**: OPD tokens linking users and centers via foreign keys (`id`, `user_id`, `facility_id`, `patient_name`, `appointment_date`, `status`).
4. **`feedback`**: Community ratings (`id`, `user_name`, `rating`, `comments`, `created_at`).
5. **`emergency_profile`**: Vital medical information for first responders (`id`, `user_id`, `emergency_contact_name`, `emergency_contact_phone`, `blood_group`, `allergies`, `medications`, `medical_conditions`).

---

## 🚀 Local Setup & Installation

### Prerequisites
* Python 3.10+ installed
* Git installed

### 1. Clone the Repository
```bash
git clone [https://github.com/Tanishq1205/swasthya-connect.git](https://github.com/Tanishq1205/swasthya-connect.git)
cd swasthya-connect
