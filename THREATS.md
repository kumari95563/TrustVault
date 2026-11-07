# TrustVault – Threat Model

## 1. Project Overview

TrustVault is a secure document-sharing application developed using Python and Django. It protects confidential documents through role-based access control, document-level permissions, and audit logging.

## 2. Assets to Protect

The important assets in TrustVault are:

- Uploaded documents and their contents.
- User accounts and login credentials.
- Document ownership information.
- Document sharing permissions.
- Audit logs and activity records.
- Application secret keys and configuration.

## 3. Potential Threats and Mitigations

### Threat 1: Unauthorized Document Access

**Attack:** A viewer or another user attempts to access a document that was not shared with them.

**Impact:** Confidential information may be exposed.

**Mitigation:**
- Require authentication for protected document operations.
- Check document ownership and explicit permissions on the server.
- Restrict viewers to documents shared with them.
- Do not rely only on hiding links in the user interface.

### Threat 2: Unauthorized File Download

**Attack:** A user changes a document ID in the download URL to download another user's file.

**Impact:** Private documents may be disclosed.

**Mitigation:**
- Check the user's role, ownership, and document permission before returning a file.
- Serve private documents through an authorized download view.
- Never expose private upload folders as public static files.

### Threat 3: Permission Abuse

**Attack:** A viewer attempts to upload documents, share documents, or revoke another user's access.

**Impact:** Users may perform actions beyond their assigned roles.

**Mitigation:**
- Enforce role checks on protected server-side views.
- Restrict upload and sharing operations to authorized roles.
- Restrict owners to managing their own documents.
- Use POST requests for permission revocation.

### Threat 4: Continued Access After Revocation

**Attack:** A user tries to access a document after the owner revokes their permission.

**Impact:** A user may retain unauthorized access.

**Mitigation:**
- Delete the document permission when access is revoked.
- Check permissions again for every new download request.
- Do not depend on previously displayed links as proof of authorization.

### Threat 5: Malicious or Invalid File Upload

**Attack:** A user uploads an unsupported, oversized, or incorrectly formatted file.

**Impact:** Invalid files may create security or application reliability risks.

**Mitigation:**
- Allow only PDF, DOCX, and TXT extensions.
- Enforce a maximum file size of 5 MB.
- Perform additional content and file-format validation.
- Treat uploaded files as untrusted input.

### Threat 6: Audit Log Tampering

**Attack:** An attacker attempts to modify or delete activity records to hide unauthorized actions.

**Impact:** Investigations and accountability may be affected.

**Mitigation:**
- Generate SHA-256 hashes for audit records.
- Link records using previous and current hashes.
- Reject normal model-level updates and instance deletions.
- Provide a verification method to detect changes in the hash chain.
- Restrict audit log administration to authorized administrators.

**Limitation:** Application-level protections do not prevent every database-level modification. Production deployment should use independently protected append-only storage and appropriate database permissions.

### Threat 7: Secret Key Exposure

**Attack:** An attacker obtains application secrets from source code or a public repository.

**Impact:** Application security may be compromised.

**Mitigation:**
- Store secrets in environment variables.
- Keep `.env` out of Git using `.gitignore`.
- Never commit passwords or secret keys.
- Use secure production configuration.

## 4. Security Testing

TrustVault includes automated tests for important security conditions, including:

- Viewers cannot upload documents.
- Viewers cannot share documents.
- Owners cannot access other owners' documents.
- Unauthorized document access is restricted.
- Audit records cannot be modified through normal model operations.
- Audit hash-chain verification detects record tampering.

Run tests using:

```bash
python manage.py test
```

## 5. Remaining Security Improvements

The following improvements should be considered before production use:

- Add malware scanning for uploaded files.
- Use HTTPS in production.
- Use secure production database and file storage.
- Add rate limiting and stronger login protections.
- Protect audit records with independent append-only storage.
- Add monitoring and backup procedures.

## 6. Conclusion

TrustVault uses server-side role-based authorization, document-level permissions, protected downloads, file validation, and audit logging to reduce unauthorized document access and improve accountability.