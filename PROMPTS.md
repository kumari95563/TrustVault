# TrustVault – AI Prompt Log

This document records how AI assistance was used during the development of TrustVault. Prompt summaries are paraphrased and are not presented as exact quotations.

## 1. Django project setup and configuration

**Date:** 2026-11-01

**Prompt summary:** Help set up the Django project, configure the custom user model, and connect the accounts and documents applications.

**AI output:** Suggested Django configuration, app structure, and migration commands.

**AI mistake / limitation:** An incorrect `dotenv` import name (`load_dotenvs`) was suggested during configuration.

**Fix:** Corrected the import to `load_dotenv` and verified the project using `python manage.py check`.

**Related commit:** https://github.com/kumari95563/TrustVault/commit/c957ae1

## 2. Document upload and access control

**Date:** 2026-11-05

**Prompt summary:** Help implement secure document upload, sharing, and downloading with owner and viewer roles.

**AI output:** Suggested Django views, forms, templates, and permission checks.

**AI mistake / limitation:** Initial implementation guidance did not sufficiently emphasize testing unauthorized direct URL access.

**Fix:** Added server-side role and document permission checks and tests for unauthorized viewer actions and document ownership isolation.

**Related commit:** https://github.com/kumari95563/TrustVault/commit/c957ae1

## 3. GitHub repository setup

**Date:** 2026-11-06

**Prompt summary:** Help publish the local TrustVault Django project to a public GitHub repository.

**AI output:** Suggested Git initialization, remote configuration, commit, pull, and push commands.

**AI mistake / limitation:** The initial push instructions did not account for the README commit already present on GitHub.

**Fix:** Pulled the remote changes using `git pull --rebase origin main`, resolved the repository history, and pushed successfully.

**Related commit:** https://github.com/kumari95563/TrustVault/commit/6896540

## 4. Dependency and environment management

**Date:** 2026-11-07

**Prompt summary:** Help prepare the project dependencies and protect environment secrets before publishing the repository.

**AI output:** Suggested generating `requirements.txt`, using environment variables, and adding sensitive files to `.gitignore`.

**AI mistake / limitation:** The initial setup did not provide a complete dependency file for reproducing the environment.

**Fix:** Generated `requirements.txt` using `pip freeze` and checked that `.env`, the virtual environment, the database, and private uploaded files were ignored by Git.

**Related commit:** https://github.com/kumari95563/TrustVault/commit/1539293

## 5. Threat modelling and audit security

**Date:** 2026-11-07

**Prompt summary:** Help identify TrustVault security threats, including unauthorized document access, permission misuse, revoked access, and audit log tampering.

**AI output:** Suggested a threat model with security risks, mitigations, and remaining improvements.

**AI mistake / limitation:** A hash-linked audit log should not be described as completely tamper-proof because database-level changes can bypass ordinary model protections.

**Fix:** Documented this limitation and identified external append-only storage and stronger production database controls as future improvements.

**Related commit:** https://github.com/kumari95563/TrustVault/commit/a6a4958

---

## AI Usage Declaration

AI tools were used as development assistance for code suggestions, debugging, documentation, test planning, and Git commands. The generated suggestions were reviewed, tested, and corrected during implementation.

AI assistance did not replace testing or security verification. The project was tested locally, and the automated test suite passed 19 tests.

**Note:** The current implementation still requires further production hardening, including additional security tests and deployment configuration.