The purpose of this project is to create a learning management system (LMS) that is designed around the learner. It will individualize learning and use AI tools to assist each student in reaching their full potential. Human instructors will be coaches and facilitators in the 
system to help them reach their full potential. Administrator role is to manage user and course databases.

## Setup

### Virtual environment and dependencies

Create and use a virtual environment, then install dependencies:

```bash
# Create virtual environment (if not already created)
python -m venv .venv

# Activate it:
#   Windows (PowerShell): .venv\Scripts\Activate.ps1
#   Windows (cmd):        .venv\Scripts\activate.bat
#   macOS/Linux:          source .venv/bin/activate

pip install -r requirements.txt
```

Dependencies include Django 4.2.7, Pillow, and python-decouple (see `requirements.txt`).

## Test accounts

You can create test users (admin, instructors, students) for local development and demos.

### Create test accounts

From the project root:

```bash
# Activate the project's .venv first (see Setup above), then:

python manage.py seed_test_accounts
```

To also create a sample course and assign an instructor and enroll two students:

```bash
python manage.py seed_test_accounts --with-course
```

Optional: use a custom password for all test accounts:

```bash
python manage.py seed_test_accounts --password mypassword
```

**Default password for all test accounts:** `testpass123`

### Test account list

| Role      | Email                         | Name             | Student/ID  |
|-----------|-------------------------------|------------------|-------------|
| Admin     | admin@neurons-lms.test        | Alex Admin       | ADMIN001    |
| Instructor| instructor@neurons-lms.test   | Jordan Instructor| INST001     |
| Instructor| instructor2@neurons-lms.test  | Sam Coach        | INST002     |
| Student   | student@neurons-lms.test      | Casey Student    | STU001      |
| Student   | student2@neurons-lms.test     | Morgan Learner   | STU002      |
| Student   | student3@neurons-lms.test     | Riley Demo       | STU003      |

The command skips any user that already exists (same username/email), so it is safe to run multiple times.
