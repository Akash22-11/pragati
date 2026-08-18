# Pragati

**Pragati** is a centralized student activity and verification platform for managing academic and extracurricular achievements.

Students can submit certificates, internships, projects, competitions, research, and other activities. Faculty and administrators can review and verify submissions, while verified records can be authenticated through **QR codes and verification hashes**.

---

## Overview

Student achievements are often distributed across certificates, emails, spreadsheets, and departmental records. Pragati provides a single system to:

* Submit and manage student activities
* Upload supporting documents
* Review submissions through role-based workflows
* Verify the authenticity of records
* Generate QR-based verification links
* Export verified records as PDFs
* Track activity and verification statistics
* Notify users about submission status changes

---

## Core Features

### Role-Based Access

Three primary roles are supported:

| Role        | Responsibilities                                                   |
| ----------- | ------------------------------------------------------------------ |
| **Student** | Submit activities, upload proofs, track verification status        |
| **Faculty** | Review and verify student submissions                              |
| **Admin**   | Manage users, activities, verification and system-level operations |

### Activity Management

Students can submit:

* Certifications
* Internships
* Projects
* Competitions
* Research
* Extracurricular activities
* Other achievements

Each submission can contain supporting documents and relevant metadata.

### Verification Workflow

```text
Student Submission
       ↓
     Pending
       ↓
Faculty / Admin Review
       ↓
 ┌─────┼─────────┐
 ↓     ↓         ↓
Approve Reject   Return
 ↓
Verification Hash
 ↓
QR Code
 ↓
Verified Record
```

Approved records receive a unique verification hash that can be used to verify their integrity.

### QR Verification

Verified activities can be represented using QR codes.

A verifier can scan the QR code and access the corresponding verification information without manually searching through student records.

### PDF Generation

Verified activity records can be exported as PDF documents using **ReportLab**.

### Real-Time Notifications

**Socket.IO** provides real-time updates when important events occur, such as:

* Submission approval
* Submission rejection
* Submission returned for correction
* Other status changes

### File Storage

Certificates and supporting documents are stored using **Cloudinary**, keeping large files outside the application server.

### Analytics

The platform can provide statistics such as:

* Total submissions
* Pending submissions
* Verified submissions
* Rejected submissions
* Activity distribution
* Verification trends

---

# Architecture

Pragati follows a layered backend architecture:

```text
Frontend
   │
   │ HTTP / WebSocket
   ▼
FastAPI
   │
   ├── Authentication & Authorization
   ├── Submission Management
   ├── Verification
   ├── Notifications
   ├── PDF / QR Generation
   └── File Management
   │
   ├───────────────┐
   ▼               ▼
PostgreSQL      Cloudinary
   │
   ▼
Student & Activity Data
```

### Backend Layers

```text
Routers
   ↓
Services
   ↓
Models / Database
```

* **Routers** handle HTTP requests and responses.
* **Services** contain business logic.
* **Models** represent database entities.
* **Schemas** validate API input and output.
* **Dependencies** handle authentication and role-based authorization.

This separation keeps business logic independent from the API layer.

---

# Tech Stack

## Backend

| Technology            | Purpose                 |
| --------------------- | ----------------------- |
| **Python**            | Backend language        |
| **FastAPI**           | REST API framework      |
| **SQLAlchemy**        | ORM                     |
| **PostgreSQL**        | Relational database     |
| **Alembic**           | Database migrations     |
| **JWT**               | Authentication          |
| **Passlib**           | Password hashing        |
| **Socket.IO**         | Real-time communication |
| **Cloudinary**        | File storage            |
| **ReportLab**         | PDF generation          |
| **QRCode**            | QR generation           |
| **Pandas / OpenPyXL** | Data export             |

## Frontend

* HTML
* CSS
* Vanilla JavaScript

## CI/CD

* GitHub Actions
* Automated tests/checks
* Pull request validation
* Security scanning
* Deployment workflows

---

# Project Structure

```text
pragati/
│
├── backend/
│   ├── main.py
│   │
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── dependencies/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── socket.py
│   │
│   ├── alembic/
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── pages/
    ├── js/
    └── css/
```

### Important Modules

| Module          | Responsibility              |
| --------------- | --------------------------- |
| `routers/`      | API endpoints               |
| `services/`     | Business logic              |
| `models/`       | SQLAlchemy database models  |
| `schemas/`      | Pydantic validation schemas |
| `dependencies/` | Authentication and RBAC     |
| `database.py`   | Database configuration      |
| `socket.py`     | Socket.IO configuration     |
| `alembic/`      | Database migrations         |

---

# Authentication & Authorization

Pragati uses **JWT-based authentication**.

The authentication flow is:

```text
Login
  ↓
Credentials Validation
  ↓
JWT Token
  ↓
Authenticated Request
  ↓
Role Verification
  ↓
Protected Resource
```

Role-based dependencies ensure that users can only access operations permitted for their role.

Passwords are stored using secure password hashing rather than plaintext values.

---

# API

| Endpoint         | Purpose                                |
| ---------------- | -------------------------------------- |
| `/auth`          | Registration, login and token refresh  |
| `/submissions`   | Create and manage activity submissions |
| `/profile`       | User profile management                |
| `/notifications` | Notification management                |
| `/uploads`       | File upload operations                 |
| `/pdf`           | PDF generation                         |
| `/health`        | Application health check               |

FastAPI automatically provides interactive API documentation:

```text
/docs
```

---

# Database

PostgreSQL is used as the primary relational database.

The database stores information such as:

* Users
* Roles
* Student activities
* Verification status
* Verification hashes
* Submission metadata
* Notification records

**SQLAlchemy** handles database interaction while **Alembic** manages schema migrations.

---

# Getting Started

## Requirements

* Python 3.10+
* PostgreSQL
* Git

## Clone

```bash
git clone https://github.com/YOUR_USERNAME/pragati.git
cd pragati
```

## Backend

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

Create:

```text
backend/.env
```

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

> Never commit `.env` or production credentials to the repository.

---

## Database Migration

```bash
alembic upgrade head
```

## Start Backend

```bash
uvicorn main:app --reload
```

API:

```text
http://localhost:8000
```

Documentation:

```text
http://localhost:8000/docs
```

---

# Frontend

The frontend is a static application.

```bash
cd frontend
python -m http.server 5500
```

Open:

```text
http://localhost:5500
```

---

# Data & Verification Flow

A typical activity lifecycle:

```text
Create Activity
      ↓
Upload Proof
      ↓
Submission Stored
      ↓
Faculty/Admin Review
      ↓
Verification
      ↓
Hash Generated
      ↓
QR Generated
      ↓
Verified Record
      ↓
PDF / Digital Verification
```

This creates a traceable lifecycle from **submission → review → verification → authentication**.

---

# Security Considerations

Pragati incorporates:

* JWT authentication
* Password hashing
* Role-based authorization
* Protected API endpoints
* Environment-based secrets
* Verification hashes
* Cloud-based document storage
* CI/CD security scanning

Sensitive configuration should always be supplied through environment variables.

---

# Development

### Create a feature branch

```bash
git checkout -b feature/your-feature
```

### Commit changes

```bash
git add .
git commit -m "feat: describe your change"
```

### Push

```bash
git push origin feature/your-feature
```

Then open a Pull Request.

For major architectural changes, open an issue before implementation.

---

# Roadmap

* [ ] Advanced analytics
* [ ] Improved document validation
* [ ] Bulk verification
* [ ] Digital student portfolio generation
* [ ] Institution-level dashboards
* [ ] Advanced QR verification
* [ ] Automated certificate metadata extraction
* [ ] AI-assisted document classification
* [ ] Mobile-first interface

---

# License

This project is licensed under the **MIT License**.

See [`LICENSE`](LICENSE) for more information.

---

<p align="center">
  <strong>Pragati — Structured. Verifiable. Digital.</strong>
</p>
