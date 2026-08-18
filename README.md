# 🎓 Pragati

<p align="center">
  <strong>Centralized Student Activity & Verification Platform</strong>
</p>

<p align="center">
  A digital platform to submit, verify, manage and authenticate student achievements.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Socket.IO-010101?style=for-the-badge&logo=socket.io&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary&logoColor=white"/>
  <img src="https://img.shields.io/badge/Alembic-4B5563?style=flat-square"/>
  <img src="https://img.shields.io/badge/ReportLab-111827?style=flat-square"/>
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white"/>
</p>

---

## 📌 About Pragati

**Pragati** is a centralized student activity record platform designed to digitize the way educational institutions collect, verify, and manage student achievements.

Students can submit proof of **certifications, internships, projects, competitions, research, extracurricular activities**, and other achievements.

Faculty and administrators can review these submissions through a structured verification workflow. Once verified, records receive a **tamper-evident verification hash and QR code**, allowing their authenticity to be checked independently.

### The goal

Instead of keeping student achievements scattered across:

`Certificates` • `Emails` • `Spreadsheets` • `Drive Folders` • `Department Records`

Pragati provides a centralized and verifiable digital record.

---

## ✨ Features

### 👨‍🎓 Student Management

Students can:

* Create and manage their profile
* Submit academic and extracurricular activities
* Upload certificates and supporting documents
* Track submission status
* Receive real-time notifications
* Access verified records
* Generate PDF records

### 🧑‍🏫 Faculty & Admin Verification

Authorized users can:

* View pending submissions
* Review uploaded evidence
* Approve submissions
* Reject submissions
* Return submissions for correction
* Monitor verification activity
* Manage student records

### 🔐 Verification & Authenticity

Every approved submission generates a unique **verification hash**.

Verified records can also be represented using a **QR code**, allowing anyone with access to the verification endpoint to validate the record.

### 📄 PDF Generation

Verified student activity records can be converted into structured PDF documents using **ReportLab**.

### ⚡ Real-Time Notifications

Pragati uses **Socket.IO** to notify users when important events occur.

For example:

```text
Faculty approves submission
        ↓
Backend updates status
        ↓
Socket.IO event
        ↓
Student receives notification
```

### ☁️ File Management

Certificates and supporting documents are uploaded to **Cloudinary**, keeping application storage separate from file storage.

### 📊 Analytics

The system can track:

* Total submissions
* Pending submissions
* Verified submissions
* Rejected submissions
* Activity categories
* Verification statistics

---

# 🏗️ Architecture

Pragati follows a layered backend architecture designed to keep API handling, business logic, and database operations separated.

```text
                         ┌──────────────────┐
                         │     Frontend     │
                         │ HTML • CSS • JS  │
                         └────────┬─────────┘
                                  │
                           HTTP / WebSocket
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     FastAPI      │
                         │    REST API      │
                         └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              │                   │                   │
              ▼                   ▼                   ▼
        Authentication       Submissions        Notifications
        & Authorization      & Verification       Socket.IO
              │                   │
              └───────────┬───────┘
                          ▼
                   ┌───────────────┐
                   │  PostgreSQL   │
                   └───────────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      ┌──────────────┐          ┌──────────────┐
      │  Cloudinary  │          │ PDF / QR     │
      │ File Storage │          │ Generation   │
      └──────────────┘          └──────────────┘
```

---

# 🔄 Verification Workflow

```text
Student
   │
   ▼
Submit Activity
   │
   ▼
Upload Evidence
   │
   ▼
┌─────────────┐
│   PENDING   │
└──────┬──────┘
       │
       ▼
Faculty / Admin Review
       │
   ┌───┼────────┐
   │   │        │
   ▼   ▼        ▼
Approve Reject  Return
   │              │
   │              └──→ Student Correction
   │
   ▼
Generate Verification Hash
   │
   ▼
Generate QR Code
   │
   ▼
Verified Activity
   │
   ├──────────────┐
   ▼              ▼
PDF Export    QR Verification
```

---

# 🛠️ Tech Stack

## Backend

| Technology     | Purpose                     |
| -------------- | --------------------------- |
| **Python**     | Core backend language       |
| **FastAPI**    | REST API framework          |
| **SQLAlchemy** | Database ORM                |
| **Alembic**    | Database migrations         |
| **PostgreSQL** | Primary relational database |
| **JWT**        | Authentication              |
| **Passlib**    | Password hashing            |
| **Socket.IO**  | Real-time communication     |
| **Cloudinary** | Certificate/file storage    |
| **ReportLab**  | PDF generation              |
| **qrcode**     | QR code generation          |
| **Pandas**     | Data processing/export      |
| **OpenPyXL**   | Excel export                |

## Frontend

```text
HTML5
CSS3
Vanilla JavaScript
```

The frontend communicates with the FastAPI backend through REST APIs and Socket.IO.

## DevOps

```text
GitHub Actions
    │
    ├── Backend CI
    ├── Pull Request Checks
    ├── Security Scanning
    └── Deployment
```

---

# 📂 Project Structure

```text
pragati/
│
├── backend/
│   ├── main.py
│   │
│   ├── app/
│   │   ├── routers/
│   │   │   └── API route definitions
│   │   │
│   │   ├── services/
│   │   │   ├── authentication
│   │   │   ├── submissions
│   │   │   ├── verification
│   │   │   ├── PDF generation
│   │   │   ├── QR generation
│   │   │   └── email
│   │   │
│   │   ├── models/
│   │   │   └── SQLAlchemy models
│   │   │
│   │   ├── schemas/
│   │   │   └── Pydantic schemas
│   │   │
│   │   ├── dependencies/
│   │   │   └── Authentication & RBAC
│   │   │
│   │   ├── config.py
│   │   ├── database.py
│   │   └── socket.py
│   │
│   ├── alembic/
│   │   └── Database migrations
│   │
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── pages/
    │   ├── login
    │   ├── dashboard
    │   ├── queue
    │   └── verify
    ├── js/
    │   └── API & authentication logic
    └── css/
```

---

# 🔑 Authentication & Authorization

Pragati uses **JWT-based authentication** combined with role-based access control.

```text
Login
  ↓
Validate Credentials
  ↓
Generate JWT
  ↓
Client Stores Token
  ↓
Authenticated API Request
  ↓
Verify Token
  ↓
Check User Role
  ↓
Allow / Deny Access
```

### Roles

```text
STUDENT
   │
   ├── Create submissions
   ├── Upload documents
   └── Track own records

FACULTY
   │
   ├── Review submissions
   ├── Verify activities
   └── Manage verification queue

ADMIN
   │
   ├── System management
   ├── User management
   └── Verification oversight
```

---

# 🗄️ Data Layer

PostgreSQL acts as the primary source of structured application data.

SQLAlchemy provides ORM-based database access, while Alembic manages schema changes.

The database contains information related to:

* Users
* Roles
* Student profiles
* Activity submissions
* Verification status
* Verification hashes
* Notifications
* Uploaded document metadata

Large certificate files are stored separately in Cloudinary while their references are maintained in the database.

---

# 🔌 API Overview

| Endpoint         | Description                             |
| ---------------- | --------------------------------------- |
| `/auth`          | Registration, login & token refresh     |
| `/submissions`   | Create, retrieve and manage submissions |
| `/profile`       | Student/user profile management         |
| `/notifications` | Notification management                 |
| `/uploads`       | Certificate and file uploads            |
| `/pdf`           | PDF generation                          |
| `/health`        | Application health check                |

FastAPI automatically provides interactive API documentation through:

```text
http://localhost:8000/docs
```

---

# 📊 Data Flow

```text
Student
   │
   ├── Activity Information
   │
   └── Supporting Certificate
              │
              ▼
         Cloudinary
              │
              ▼
          FastAPI API
              │
              ▼
          PostgreSQL
              │
              ▼
       Faculty / Admin
              │
        ┌─────┴─────┐
        ▼           ▼
    Approved      Rejected
        │
        ▼
 Verification Hash
        │
        ├──────→ QR Code
        │
        └──────→ PDF Record
```

---

# 🚀 Getting Started

## Prerequisites

* Python **3.10+**
* PostgreSQL
* Git

## Clone

```bash
git clone https://github.com/YOUR_USERNAME/pragati.git
cd pragati
```

## Backend Setup

```bash
cd backend

python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside `backend/`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/pragati

JWT_SECRET=your-secret-key

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

MAIL_EMAIL=your-email@example.com
MAIL_PASSWORD=your-app-password

ADMIN_EMAIL=admin@example.com
```

> **Important:** Never commit `.env` files or production credentials to GitHub.

---

## Database Migration

```bash
alembic upgrade head
```

## Run Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

---

# 🌐 Frontend Setup

The frontend is a static HTML/CSS/JavaScript application.

```bash
cd frontend
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

# 🔒 Security

Pragati includes several security mechanisms:

* JWT authentication
* Password hashing
* Role-based authorization
* Protected API routes
* Environment-based configuration
* Verification hashes
* Secure cloud file storage
* CI/CD security checks

Sensitive credentials should always be supplied through environment variables.

---

# 📈 Future Roadmap

* [ ] Advanced analytics dashboard
* [ ] Bulk submission verification
* [ ] Digital student portfolio generation
* [ ] Institution-wide dashboards
* [ ] Advanced QR verification portal
* [ ] Automated certificate metadata extraction
* [ ] AI-assisted document classification
* [ ] Improved reporting and exports
* [ ] Mobile-first interface

---

# 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

Then open a Pull Request.

For major changes, please open an issue first to discuss the proposed implementation.

---

# 📜 License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for details.

---

<p align="center">
  <strong>Pragati — One platform for every achievement.</strong>
</p>

<p align="center">
  Built with Python • FastAPI • PostgreSQL • JavaScript
</p>
