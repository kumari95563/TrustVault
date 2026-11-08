# TrustVault – AI Prompt Log

This document records how AI assistance was used during the development of TrustVault. Prompt summaries are paraphrased and are not presented as exact quotations.

## 1. Django Project Setup and Configuration

**Date:** 2026-11-01

**Prompt Summary:**  
Help set up the Django project, configure the custom user model, and connect the accounts and documents applications.

**AI Output:**  
Provided Django project setup instructions, application configuration, custom user model guidance, and database migration commands.

**AI Mistake:**  
Initially suggested an incorrect environment-loading function (`load_dotenvs`).

**Fix:**  
Corrected it to use `load_dotenv` and verified that the project settings loaded correctly.

## 2. Document Upload and Access Control

**Date:** 2026-11-02

**Prompt Summary:**  
Implement secure document upload, document listing, sharing permissions, and protected downloads for document owners and viewers.

**AI Output:**  
Provided Django models, views, URL configuration, templates, and server-side permission checks.

**AI Limitation:**  
Initial guidance did not sufficiently emphasize testing direct download URLs after permission revocation.

**Fix:**  
Added server-side authorization checks and tested direct URL access. Unauthorized users receive HTTP 403 Forbidden.

## 3. GitHub Repository Setup

**Date:** 2026-11-03

**Prompt Summary:**  
Help configure Git, create a GitHub repository, commit project files, and push the Django application.

**AI Output:**  
Provided Git commands and repository setup guidance.

**AI Mistake:**  
The local and remote repositories initially had different commit histories.

**Fix:**  
Used `git pull --rebase origin main` to synchronize the histories before pushing changes.

## 4. Dependency and Environment Management

**Date:** 2026-11-04

**Prompt Summary:**  
Help manage Python dependencies, create requirements.txt, and protect environment variables and sensitive configuration.

**AI Output:**  
Provided dependency management instructions and `.gitignore` configuration.

**Fix:**  
Created a requirements file and excluded sensitive environment files from Git tracking.

## 5. Threat Modeling and Audit Trail Security

**Date:** 2026-11-05

**Prompt Summary:**  
Improve TrustVault security by implementing audit logging, denied-access tracking, and audit integrity verification.

**AI Output:**  
Provided audit logging guidance and a SHA-256 hash-chain verification approach.

**AI Limitation:**  
A hash chain alone does not guarantee complete protection against privileged database-level modifications.

**Fix:**  
Added hash-chain verification and documented the remaining security limitations. Further hardening, such as external immutable audit storage, is a possible future improvement.

## 6. Secure Invitation-Based Registration

**Date:** 2026-11-07

**Prompt Summary:**  
Implement administrator-controlled user registration through secure invitation links with assigned roles.

**AI Output:**  
Provided invitation model, invitation creation, registration views, templates, URL configuration, and test cases.

**AI Limitation:**  
The initial implementation required additional verification for invitation reuse, expiration, and unauthorized invitation creation.

**Fix:**  
Added one-time invitation validation, 24-hour expiration, server-side role assignment, access restrictions, and invitation tests.

**Related Commit:** `9c3dd33`

## 7. Password Reset and Email Configuration

**Date:** 2026-11-08

**Prompt Summary:**  
Implement password reset functionality, configure email delivery, and record successful password resets in the audit trail.

**AI Output:**  
Provided Django password reset views, templates, Gmail SMTP configuration, and password-reset audit logging.

**AI Limitation:**  
Gmail SMTP worked locally, but live email delivery failed on Render Free because outbound SMTP port 587 is restricted.

**Fix / Remaining Limitation:**  
Kept the password reset implementation and documented the live email delivery limitation. Admin-managed password changes through Django Admin are available as an alternative. Live self-service email password reset is not currently confirmed working.

**Related Commit:** `9c3dd33`

## Testing and Verification

The project was tested locally using Django's automated test framework.

- **Total test cases passed:** 24
- Admin, Owner, and Viewer login tested.
- Document upload and sharing tested.
- Viewer download permission tested.
- Permission revocation tested.
- Direct download after revocation tested (HTTP 403).
- Denied-access audit logging tested.
- Invitation creation and registration tested.
- Invitation reuse and expiration tested.
- Audit hash-chain verification tested.

## AI Usage Declaration

AI tools were used as development assistants for understanding Django concepts, debugging errors, generating initial code suggestions, improving security checks, and preparing test cases.

The generated suggestions were reviewed, modified, integrated, and tested during development. AI assistance was not treated as a replacement for understanding or verifying the implementation.

The developer remains responsible for the submitted code, project functionality, testing, and explanation of the implementation.