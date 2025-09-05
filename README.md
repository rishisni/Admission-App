# Admission Portal - README & FRD

---

## Project Overview
The Admission Portal is a web application for student admission management. Students can submit applications, upload documents, and track their application status. Admins can review, approve, or reject applications, and generate PDF admission letters for approved applications.

---

## Functional Requirement Document (FRD)

### 1. Application Form
- Fields: Name, Email, Phone, Address, Academic Details.
- File Uploads: ID Proof, Degree Certificate.
- Validation: Required fields, email format, file type (pdf/png/jpg/jpeg).

### 2. Admin Review
- Admin Dashboard: List all applications.
- Actions: Approve, Reject.
- On Approval: Generate PDF admission letter containing student details.
- On Rejection: Update status.

### 3. Student Tracking
- Track by Application ID or Email.
- Status Display:
  - Pending: "Your application is under review."
  - Approved: Download PDF admission letter.
  - Rejected: "Better luck next time!"

### 4. Database
- Relational database (MySQL/PostgreSQL).
- Tables:
  - `applications`: stores student info, file paths, status, PDF path.

### 5. File Management
- Uploads stored in `static/uploads/`.
- PDF generated using ReportLab with proper formatting.
- Filenames include timestamp to avoid duplicates.

### 6. Security & Validation
- Unique email per student.
- Required fields validated.
- Only approved applications can download PDF.

---

## Installation Instructions

```bash
git clone <repo-url>
cd admission_app
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
