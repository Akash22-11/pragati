# 🎓 Pragati

<p align="center">
  <strong>Centralized Student Activity & Verification Platform</strong>
</p>

<p align="center">
  <em>One platform to submit, verify, track, and authenticate student achievements.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" />
  <img src="https://img.shields.io/badge/Socket.IO-010101?style=for-the-badge&logo=socket.io&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary&logoColor=white" />
  <img src="https://img.shields.io/badge/ReportLab-111827?style=flat-square" />
  <img src="https://img.shields.io/badge/Alembic-4B5563?style=flat-square" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" />
</p>

---

## 🧭 Overview

**Pragati** is a centralized platform for managing and verifying student achievements.

Students can submit proof of their:

* 🎓 Certifications
* 💼 Internships
* 💻 Projects
* 🏆 Competitions
* 🔬 Research
* 🎨 Extracurricular activities
* 📁 Other academic achievements

Faculty and administrators can then **review, approve, reject, or return submissions** through a structured verification workflow.

Once verified, every record receives a **tamper-evident verification hash and QR code**, allowing its authenticity to be checked instantly.

> **Pragati transforms scattered student achievement records into a structured, verifiable digital portfolio.**

---

# ✨ Key Features

<table>
<tr>

<td width="50%" valign="top">

### 👥 Role-Based Access

Dedicated workflows for:

* 👨‍🎓 Students
* 👨‍🏫 Faculty
* 🛡️ Administrators

Each role receives appropriate permissions and functionality.

</td>

<td width="50%" valign="top">

### 📑 Activity Management

Students can submit evidence across multiple activity categories with supporting documents.

</td>

</tr>

<tr>

<td width="50%" valign="top">

### ✅ Verification Workflow

Faculty and administrators can:

* Approve submissions
* Reject submissions
* Return submissions for corrections
* Track verification status

</td>

<td width="50%" valign="top">

### 🔐 Tamper-Evident Records

Verified submissions generate a unique verification hash that can be used to establish record authenticity.

</td>

</tr>

<tr>

<td width="50%" valign="top">

### 📱 QR Verification

Every verified activity can generate a scannable QR code for quick authenticity verification.

</td>

<td width="50%" valign="top">

### 📄 PDF Records

Verified student activity records can be exported as structured PDF documents.

</td>

</tr>

<tr>

<td width="50%" valign="top">

### ⚡ Real-Time Notifications

Socket.IO enables real-time updates when submission statuses change.

</td>

<td width="50%" valign="top">

### 📊 Analytics

Dashboards provide insights into:

* Submission volumes
* Verification activity
* Approval/rejection statistics
* Student activity records

</td>

</tr>
</table>

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │       STUDENT       │
                         │                     │
                         │ Submit Activities   │
                         │ Upload Documents    │
                         │ Track Status        │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FRONTEND       │
                         │                     │
                         │ HTML • CSS • JS     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │      FASTAPI        │
                         │      BACKEND        │
                         │                     │
                         │ Auth                │
                         │ Submissions         │
                         │ Verification        │
                         │ Notifications       │
                         └──────┬──────┬───────┘
                                │      │
                    ┌───────────┘      └────────────┐
                    ▼                               ▼
          ┌─────────────────┐              ┌─────────────────┐
          │   PostgreSQL    │              │   Cloudinary    │
          │                 │              │                 │
          │ Users           │              │ Certificates    │
          │ Activities      │              │ Attachments     │
          │ Verification    │              │                 │
          └─────────────────┘              └─────────────────┘
                    │
                    ▼
          ┌─────────────────────┐
          │ PDF + QR Generation │
          │                     │
          │ ReportLab + QRCode  │
          └─────────────────────┘
```

---

# 🔐 Verification Flow

```text
Student
   │
   │ Submit certificate / proof
   ▼
┌───────────────┐
│   PENDING     │
└───────┬───────┘
        │
        ▼
┌──────────────────────┐
│ Faculty / Admin      │
│ Review Submission    │
└──────────┬───────────┘
           │
     ┌─────┼─────┐
     │     │     │
     ▼     ▼     ▼
 APPROVE REJECT RETURN
     │
     ▼
Verification Hash
     │
     ▼
QR Code Generated
     │
     ▼
Verified Digital Record
```

---

# 🛠️ Tech Stack

## Backend

| Technology            | Purpose                      |
| :-------------------- | :--------------------------- |
| **FastAPI**           | REST API framework           |
| **Python**            | Backend programming language |
| **SQLAlchemy**        | ORM & database interaction   |
| **Alembic**           | Database migrations          |
| **PostgreSQL**        | Primary database             |
| **JWT**               | Authentication               |
| **Passlib**           | Password hashing             |
| **Socket.IO**         | Real-time communication      |
| **Cloudinary**        | File & certificate storage   |
| **ReportLab**         | PDF generation               |
| **QRCode**            | QR generation                |
| **Pandas / OpenPyXL** | Data export                  |

## Frontend

* HTML5
* CSS3
* Vanilla JavaScript

## DevOps / CI/CD

* GitHub Actions
* Automated backend checks
* Pull request validation
* Security scanning
* Deployment workflows

---

# 📂 Project Structure

```text
pragati/
│
├── backend/
│   │
│   ├── main.py
│   │
│   ├── app/
│   │   ├── routers/
│   │   │   └── API route definitions
│   │   │
│   │   ├── services/
│   │   │   ├── auth
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
    │
    ├── index.html
    │
    ├── pages/
    │   ├── login
    │   ├── dashboard
    │   ├── queue
    │   └── verify
    │
    ├── js/
    │   └── API client & authentication
    │
    └── css/
```

---

# 🚀 Getting Started

## Prerequisites

Make sure you have installed:

* **Python 3.10+**
* **PostgreSQL**
* **Git**

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/pragati.git
cd pragati
```

---

## 2️⃣ Create Virtual Environment

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

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create:

```text
backend/.env
```

Add:

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

> ⚠️ Never commit `.env` files or real credentials to GitHub.

---

## 5️⃣ Run Database Migrations

```bash
alembic upgrade head
```

---

## 6️⃣ Start the Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

---

# 🌐 Frontend

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

# 🔌 API Overview

| Endpoint         | Purpose                              |
| :--------------- | :----------------------------------- |
| `/auth`          | Registration, login & token refresh  |
| `/submissions`   | Create & manage activity submissions |
| `/profile`       | User profile management              |
| `/notifications` | Notification management              |
| `/uploads`       | Certificate & file uploads           |
| `/pdf`           | PDF record generation                |
| `/health`        | Application health check             |

FastAPI automatically generates interactive documentation at:

```text
/docs
```

---

# 🔒 Security

Pragati implements several security-focused mechanisms:

* 🔐 JWT-based authentication
* 🔑 Password hashing
* 👥 Role-based authorization
* 🛡️ Protected API routes
* 🔏 Verification hashes
* 📁 Secure cloud file storage
* 🔍 Security scanning through CI/CD
* 🌐 Environment-based secret management

---

# ⚡ Real-Time Architecture

Pragati uses **Socket.IO** to provide real-time updates.

For example:

```text
Faculty approves submission
          │
          ▼
      Backend
          │
          ▼
     Socket.IO
          │
          ▼
       Student
          │
          ▼
 "Your submission has been verified."
```

This removes the need for users to constantly refresh their dashboard.

---

# 📊 Data Flow

```text
Student
   │
   ▼
Create Submission
   │
   ▼
Upload Certificate
   │
   ▼
Cloudinary
   │
   ▼
PostgreSQL
   │
   ▼
Faculty Review
   │
   ├───────────────┐
   ▼               ▼
Approved         Rejected
   │
   ▼
Verification Hash
   │
   ▼
QR Code
   │
   ▼
Verified Record
   │
   ├───────────────┐
   ▼               ▼
PDF Export      QR Verification
```

---

# 🤝 Contributing

Contributions are welcome.

### 1. Fork the repository

```bash
git clone https://github.com/YOUR_USERNAME/pragati.git
```

### 2. Create a feature branch

```bash
git checkout -b feature/your-feature
```

### 3. Commit your changes

```bash
git commit -m "feat: add your feature"
```

### 4. Push the branch

```bash
git push origin feature/your-feature
```

### 5. Open a Pull Request

For significant changes, please open an issue first to discuss the proposed implementation.

---

# 🗺️ Future Roadmap

* [ ] Mobile-responsive dashboard improvements
* [ ] Advanced analytics
* [ ] Institution-wide student profiles
* [ ] Digital student portfolio generation
* [ ] Advanced document validation
* [ ] Bulk verification workflows
* [ ] Excel/CSV reporting improvements
* [ ] Enhanced QR verification portal
* [ ] Automated certificate metadata extraction
* [ ] AI-assisted document classification

---

# 💡 Why Pragati?

Traditional student achievement records are often scattered across:

```text
Emails
   +
Google Drive
   +
Paper Certificates
   +
Spreadsheets
   +
Department Records
```

Pragati brings them together:

```text
                ┌──────────────────────┐
                │       PRAGATI        │
                ├──────────────────────┤
                │ Activities           │
                │ Verification         │
                │ Documents            │
                │ Analytics             │
                │ QR Authentication    │
                │ PDF Records           │
                └──────────────────────┘
```

> **One platform. One student record. Verifiable achievements.**

---

# 📜 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

<p align="center">

### 🚀 Pragati

<strong>Building a better way to manage and verify student achievements.</strong>

<br><br>

Made with ❤️ using Python, FastAPI & PostgreSQL.

</p>
