# 🔐 TrustVault – Secure Document Sharing with Audit Trail

TrustVault is a secure document management and sharing platform built using Python and Django. It allows administrators and document owners to manage documents, share them with authorized users, control permissions, and track important activities through an audit trail.

## 🎯 Project Objective

To ensure that documents are accessible only to authorized users and that important document activities are recorded for accountability and security.

## 🚀 Key Features

- **Role-Based Access Control:** Administrator, Document Owner, and Viewer roles.
- **Secure Document Upload:** Supports PDF, DOCX, and TXT files with file validation.
- **Document Management:** Upload and manage documents.
- **Secure Sharing:** Owners can share documents with authorized viewers.
- **Permission Management:** READ and EDIT permission levels.
- **Access Revocation:** Owners and administrators can revoke document permissions.
- **Protected Downloads:** Server-side permission checks before document downloads.
- **Invitation-Based Registration:** Administrators can invite users with assigned roles.
- **One-Time Invitations:** Invitation links expire after 24 hours and cannot be reused.
- **Audit Trail:** Records important activities such as upload, share, download, revoke, invitation creation, registration, and denied access.
- **Audit Integrity:** SHA-256 hash chaining helps detect modifications to audit records.
- **Password Management:** Django password reset functionality is implemented; live email delivery has a deployment limitation described below.
- **Automated Tests:** Includes tests for document permissions, invitations, access control, and audit functionality.

## 👥 User Roles

| Role | Permissions |
|---|---|
| Administrator | Manage users, manage invitations, access documents, and view audit logs |
| Document Owner | Upload, manage, share, and revoke access to own documents |
| Viewer | View and download documents explicitly shared with them |

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- JavaScript
- Git and GitHub
- Render

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/kumari95563/TrustVault.git
cd TrustVault
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment on Windows

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root and configure your own secret key and local settings.

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Do not share or commit your actual secret key, email credentials, or other sensitive environment variables.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/accounts/login/

## 🧪 Run Automated Tests

Run the complete Django test suite:

```bash
python manage.py test
```

**Verified test result:** 24 test cases passed in the verified test run.

## 🔒 Security Notes

- Authorization checks are performed on protected document operations.
- Unauthorized direct download requests are rejected.
- Revoked users cannot continue downloading documents using old download links.
- Invitation links are one-time use and expire after 24 hours.
- User roles are assigned server-side by the administrator.
- Important security events are recorded in the audit trail.
- SHA-256 hash chaining helps detect audit record modifications.
- Environment secrets and local database files are excluded from Git.
- The hash chain is not a substitute for independently protected, append-only production storage.

## 📧 Password Reset Limitation

Password reset functionality is implemented using Django's password reset views.

Gmail SMTP works in local development. However, live email delivery through Gmail SMTP is currently unavailable on the Render Free deployment because outbound SMTP port 587 is restricted.

Administrators can change user passwords through Django Admin as an alternative.

## 🔑 Demo Login Instructions

The application supports three user roles:

- **Administrator:** Manages users, invitations, documents, and audit records.
- **Document Owner:** Uploads documents and manages sharing permissions.
- **Document Viewer:** Accesses documents explicitly shared with them.

### How to Access

1. Open the live application: https://trustvault-hkxp.onrender.com/
2. Navigate to the login page.
3. Use the demo account credentials provided separately by the project developer.
4. Explore the features available for each role.

**Security Note:** Demo credentials are not published in this repository. Each role has separate access permissions.

## 🌐 Live Deployment

**Live Application:** https://trustvault-hkxp.onrender.com/

**GitHub Repository:** https://github.com/kumari95563/TrustVault

## 📌 Project Status

TrustVault has been developed using Django and deployed on Render.

Core functionality, role-based access control, secure document sharing, invitation-based registration, audit logging, and automated tests have been implemented and tested.

Some deployment limitations, including live password reset email delivery, are documented above.

## 👩‍💻 Developer

**GitHub:** https://github.com/kumari95563

**Project:** TrustVault – Secure Document Sharing with Audit Trail