# 🔐 TrustVault – Secure Document Sharing with Audit Trail

TrustVault is a secure document management and sharing platform built using Python and Django. It helps users upload, manage, share, and access documents with role-based permissions and audit logging.

## 🎯 Project Objective

To ensure that documents are accessible only to authorized users and that important document activities are recorded for accountability.

## 🚀 Key Features

- **Role-Based Access Control:** Administrator, Document Owner, and Viewer roles.
- **Secure Document Upload:** Supports PDF, DOCX, and TXT files with file validation.
- **Document Management:** Upload and view documents.
- **Secure Sharing:** Owners can share documents with viewers.
- **Permission Management:** READ and EDIT access levels.
- **Access Revocation:** Owners and administrators can revoke document permissions.
- **Protected Downloads:** Server-side permission checks before document downloads.
- **Audit Trail:** Records upload, share, download, and revoke activities.
- **Audit Integrity:** SHA-256 hash chaining to help detect modifications to audit records.
- **Automated Tests:** Tests for permissions, document access, and audit integrity.

## 👥 User Roles

| Role | Permissions |
|---|---|
| Administrator | Manage and access all documents; view audit logs |
| Document Owner | Upload, manage, share, and revoke access to own documents |
| Viewer | View and download documents explicitly shared with them |

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Git and GitHub

## ⚙️ Local Installation

1. Clone the repository:

```bash
git clone https://github.com/kumari95563/TrustVault.git
cd TrustVault
```

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate it on Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install Django python-dotenv python-magic-bin
```

5. Create a `.env` file in the project root and configure your own secret key:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

6. Apply migrations:

```bash
python manage.py migrate
```

7. Create an administrator account:

```bash
python manage.py createsuperuser
```

8. Start the development server:

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/accounts/login/` in your browser.

## 🧪 Run Tests

Run the complete test suite:

```bash
python manage.py test
```

## 🔒 Security Notes

- Authorization checks are performed on protected document operations.
- Private document files should be served only through authorized download views.
- Environment secrets and local database files are excluded from Git.
- The audit hash chain helps detect record tampering; it is not a substitute for independently protected, append-only production storage.

## 📌 Project Status

Local development and automated tests completed. Production deployment is a separate step.

## 👩‍💻 Developer

GitHub: https://github.com/kumari95563

## 📂 Repository

https://github.com/kumari95563/TrustVault
