<div align="center">

# 🎓 Pragati.

### One Platform for Every Achievement

A centralized platform to **submit, verify, and authenticate** student achievements — replacing scattered certificates, emails, and spreadsheets with a single verifiable digital record.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Socket.IO](https://img.shields.io/badge/Socket.IO-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)

[![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary&logoColor=white)](https://cloudinary.com/)
[![Alembic](https://img.shields.io/badge/Alembic-4B5563?style=flat-square)](https://alembic.sqlalchemy.org/)
[![ReportLab](https://img.shields.io/badge/ReportLab-111827?style=flat-square)](https://www.reportlab.com/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)

<br/>

[**Quick Start**](#-quick-start) · [**Features**](#-features) · [**Architecture**](#️-architecture) · [**API**](#-api-overview) · [**Contributing**](#-contributing)

</div>

---

## 📌 Why Pragati?

Student achievements today live everywhere *except* where they should:

<div align="center">

`📧 Emails` &nbsp;→&nbsp; `📁 Drive Folders` &nbsp;→&nbsp; `📊 Spreadsheets` &nbsp;→&nbsp; `🗄️ Department Records`

</div>

That makes verification slow, records easy to lose, and authenticity hard to prove. **Pragati** fixes this by giving institutions a single workflow: students submit proof of certifications, internships, projects, competitions, and research; faculty review and verify it; and every verified record gets a **tamper-evident hash and QR code** anyone can check.

---

## ✨ Features

<table>
<tr>
<td width="33%" valign="top">

### 👨‍🎓 For Students
- Build a personal achievement profile
- Submit activities & upload certificates
- Track submission status in real time
- Get instant notifications
- Export verified records as PDF

</td>
<td width="33%" valign="top">

### 🧑‍🏫 For Faculty & Admins
- Review pending submissions
- Approve, reject, or return for correction
- Inspect uploaded evidence
- Monitor verification activity
- Manage student records at scale

</td>
<td width="33%" valign="top">

### 🔐 Trust & Verification
- Unique verification hash per record
- Scannable QR code authentication
- Public verification endpoint
- Structured, exportable PDF records
- Full audit trail

</td>
</tr>
</table>

### ⚡ Real-Time Notifications

Powered by **Socket.IO**, so nobody has to refresh a page to know what happened:

```text
Faculty approves submission → Backend updates status → Socket.IO event → Student notified instantly
```

### ☁️ File Storage & 📊 Analytics

Certificates are uploaded to **Cloudinary**, keeping large files out of the application database. Meanwhile, the platform tracks totals, pending/verified/rejected counts, and category-level statistics — everything an institution needs to see engagement at a glance.

---

## 🏗️ Architecture

Pragati uses a layered backend that keeps API handling, business logic, and data access cleanly separated.

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

### 🔄 Verification Workflow

```text
 Student                                          
    │ Submit Activity + Upload Evidence            
    ▼                                               
 ┌─────────────┐                                    
 │   PENDING   │                                    
 └──────┬──────┘                                    
        │ Faculty / Admin Review                    
    ┌───┼────────────┐                              
    ▼   ▼             ▼                             
 Approve Reject     Return → back to Student        
    │                                                
    ▼                                                
 Generate Verification Hash → Generate QR Code       
    │                                                
    ▼                                                
 ✅ Verified Activity → PDF Export & QR Verification 
```

### 🔑 Authentication & Roles

Pragati uses **JWT-based authentication** with role-based access control (RBAC):

| Role | Can do |
|---|---|
| 🎓 **Student** | Create submissions, upload documents, track own records |
| 🧑‍🏫 **Faculty** | Review & verify activities, manage the verification queue |
| 🛡️ **Admin** | Full system management, user management, verification oversight |

---

## 🛠️ Tech Stack

<table>
<tr>
<td valign="top">

**Backend**

| Tech | Purpose |
|---|---|
| Python | Core language |
| FastAPI | REST API framework |
| SQLAlchemy | Database ORM |
| Alembic | Migrations |
| PostgreSQL | Primary database |
| JWT + Passlib | Auth & password hashing |
| Socket.IO | Real-time events |
| Cloudinary | File storage |
| ReportLab | PDF generation |
| qrcode | QR generation |
| Pandas / OpenPyXL | Data & Excel export |

</td>
<td valign="top">

**Frontend**

- HTML5
- CSS3
- Vanilla JavaScript

Communicates with the backend via REST APIs and Socket.IO.

**DevOps**

- GitHub Actions
- Backend CI
- Pull request checks
- Security scanning
- Automated deployment

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Prerequisites

Make sure you have these installed:

- ✅ Python **3.10+**
- ✅ PostgreSQL
- ✅ Git

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pragati.git
cd pragati
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

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

> ⚠️ **Never commit `.env` files or production credentials to GitHub.**

### 4. Run database migrations

```bash
alembic upgrade head
```

### 5. Start the backend

```bash
uvicorn main:app --reload
```

Your API is now live at **http://localhost:8000** 🎉
Interactive docs (Swagger UI) at **http://localhost:8000/docs**

### 6. Start the frontend

```bash
cd frontend
python -m http.server 5500
```

Open **http://localhost:5500** in your browser.

---

## 📂 Project Structure

```text
pragati/
│
├── backend/
│   ├── main.py
│   │
│   ├── app/
│   │   ├── routers/        → API route definitions
│   │   ├── services/       → auth, submissions, verification, PDF/QR, email
│   │   ├── models/         → SQLAlchemy models
│   │   ├── schemas/        → Pydantic schemas
│   │   ├── dependencies/   → Authentication & RBAC
│   │   ├── config.py
│   │   ├── database.py
│   │   └── socket.py
│   │
│   ├── alembic/            → Database migrations
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── pages/               → login, dashboard, queue, verify
    ├── js/                  → API & authentication logic
    └── css/
```

---

## 🔌 API Overview

| Endpoint | Description |
|---|---|
| `/auth` | Registration, login & token refresh |
| `/submissions` | Create, retrieve and manage submissions |
| `/profile` | Student/user profile management |
| `/notifications` | Notification management |
| `/uploads` | Certificate and file uploads |
| `/pdf` | PDF generation |
| `/health` | Application health check |

Full interactive API documentation is auto-generated by FastAPI at `/docs`.

---

## 🗄️ Data Layer

PostgreSQL is the system of record, accessed through SQLAlchemy's ORM and versioned with Alembic migrations. It stores users, roles, student profiles, submissions, verification status/hashes, notifications, and document metadata — while the certificate files themselves live in Cloudinary, referenced by URL.

---

## 🔒 Security

- 🔑 JWT authentication
- 🔒 Password hashing (Passlib)
- 🛡️ Role-based authorization
- 🚧 Protected API routes
- 🌍 Environment-based configuration
- #️⃣ Tamper-evident verification hashes
- ☁️ Secure cloud file storage
- 🤖 CI/CD security checks

Sensitive credentials should **always** be supplied through environment variables, never hardcoded.

---

## 📈 Roadmap

- [ ] Advanced analytics dashboard
- [ ] Bulk submission verification
- [ ] Digital student portfolio generation
- [ ] Institution-wide dashboards
- [ ] Advanced QR verification portal
- [ ] Automated certificate metadata extraction
- [ ] AI-assisted document classification
- [ ] Improved reporting and exports
- [ ] Mobile-first interface

---

## 🤝 Contributing

Contributions are welcome! To get started:

```bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

Then open a Pull Request. For major changes, please open an issue first to discuss what you'd like to change.

---

## 📜 License

This project is licensed under the **MIT License** — see [`LICENSE`](LICENSE) for details.

---

<div align="center">

**Pragati — One platform for every achievement.** 🎓

Built with 🐍 Python · ⚡ FastAPI · 🐘 PostgreSQL · 🌐 JavaScript

</div>
