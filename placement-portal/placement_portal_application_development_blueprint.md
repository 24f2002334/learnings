# Placement Portal Application (PPA - V2) - Complete Development Blueprint

Welcome to your ultimate step-by-step master guide for building the **Placement Portal Application (PPA - V2)** from scratch. This blueprint breaks down the entire project lifecycle into logical, manageable phases. It explains **what** to build, **why** it is built that way, and **when** you should refer to official documentation.

---

## Phase 1: Environment Setup & Project Architecture

Before writing any feature code, you must establish a clean, compliant project structure that adheres strictly to the project constraints (Flask, Vue.js, SQLite, Redis, Celery, Bootstrap).

### 1.1 Folder Structure Setup
Create a professional project layout separating backend APIs, frontend assets, background workers, and configuration files.

```text
placement_portal/
│
├── backend/
│   ├── app.py                  # Flask application factory and extension initialization
│   ├── config.py               # Configuration for development, production, caching, database
│   ├── models.py               # SQLAlchemy database models (User, Company, Drive, Application)
│   ├── database.py             # Database instance and programmatic initialization script
│   ├── api.py                  # Flask-RESTful or Flask routes / Blueprints for API endpoints
│   ├── tasks.py                # Celery background tasks (Daily reminders, monthly reports, CSV export)
│   ├── celery_worker.py        # Celery worker entry point
│   └── requirements.txt        # Python package dependencies
│
├── frontend/
│   ├── index.html              # Single-page entry point utilizing CDN for Vue.js & Bootstrap
│   ├── static/
│   │   ├── css/                # Custom CSS styling (if needed alongside Bootstrap)
│   │   └── js/                 # Vue.js component scripts and router setup
│   └── templates/              # Jinja2 template wrapping index.html
│
├── instance/
│   └── database.sqlite3        # SQLite database file (created programmatically)
└── README.md                   # Project documentation and setup instructions
```

### 1.2 Why This Structure?
* **Separation of Concerns:** Keeping `backend/` and `frontend/` clear makes debugging easier and aligns with modern API-driven web applications.
* **Programmatic Database Creation:** The database file under `instance/` must be generated entirely via code (using `db.create_all()` inside an application context or setup script) to comply with the rule: *"Manual database creation (e.g., DB Browser for SQLite) is NOT allowed."*

### 1.3 Documentation Checkpoints
* **Flask Documentation:** Refer to the [Flask Official Documentation](https://flask.palletsprojects.com/) when setting up your application factory pattern, request context, and blueprint routing.
* **SQLAlchemy Documentation:** Refer to [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) for defining relationships (`db.relationship`, foreign keys) between Users, Companies, Drives, and Applications.

---

## Phase 2: Database Modeling & Programmatic Setup

### 2.1 Core Models Required
You need a robust relational schema to link administrators, company profiles, student records, placement drives, and job applications.

1. **Unified User Model:**
   * Fields: `id`, `email`, `password_hash`, `role` (`admin`, `company`, `student`), `is_active`, `is_blacklisted`.
2. **Company Profile Model:**
   * Fields: `id`, `user_id` (Foreign Key), `company_name`, `hr_contact`, `website`, `approval_status` (`Pending`, `Approved`, `Rejected`).
3. **Placement Drive Model:**
   * Fields: `id`, `company_id` (Foreign Key), `job_title`, `job_description`, `eligibility_branch`, `eligibility_cgpa`, `eligibility_year`, `application_deadline`, `status` (`Pending`, `Approved`, `Closed`).
4. **Application Model:**
   * Fields: `id`, `student_id` (Foreign Key), `drive_id` (Foreign Key), `application_date`, `status` (`Applied`, `Shortlisted`, `Selected`, `Rejected`).

### 2.2 Programmatic Admin Seeding
Since admin registration is prohibited, you must write a startup script that checks if an admin user exists; if not, it automatically seeds the pre-existing superuser into the database.

### 2.3 Documentation Checkpoints
* **SQLite / Python SQLite3:** Review native Python data types and constraints.
* **Flask-Security / Werkzeug Security:** Check out `werkzeug.security` (`generate_password_hash`, `check_password_hash`) to securely store user credentials.

---

## Phase 3: Authentication & Role-Based Access Control (RBAC)

### 3.1 Implementation Steps
1. Build API endpoints for student and company self-registration.
2. Implement secure login for all roles returning session cookies or tokens (JWT / Flask-Login tokens).
3. Enforce strict backend middleware/decorators ensuring only `admin` can approve companies/drives, only `company` users can post drives, and only `student` users can apply.

### 3.2 Why This Matters
Security is critical in enterprise placement systems. Unauthorized users must never access restricted management endpoints or manipulate data belonging to other organizations.

### 3.3 Documentation Checkpoints
* **Flask-Login / Flask-Security:** Review session management documentation to handle role checks cleanly.
* **JWT (JSON Web Tokens):** If using token-based auth, review PyJWT documentation for token generation and validation headers.

---

## Phase 4: Core Dashboards & Role Functionalities

### 4.1 Admin Dashboard & Controls
* **Metrics:** Display total students, companies, and active placement drives.
* **Approvals:** Endpoints to toggle company approval status and placement drive approval status.
* **Moderation:** Search functionality for students/companies and blacklisting/deactivation switches.

### 4.2 Company Dashboard & Workflow
* **Profile Submission:** Register company details pending admin approval.
* **Drive Management:** Create new drives *only* after admin approval is granted.
* **Applicant Tracking:** View student applicants, shortlist candidates, update interview results, and mark final selection status.

### 4.3 Student Dashboard & Workflow
* **Profile & Resume:** Edit personal info and upload resume documents.
* **Drive Discovery:** Browse approved placement drives with eligibility filtering (CGPA, branch, year).
* **Application & History:** Apply to drives (with strict validation preventing duplicate applications), view live status updates (`Applied` $\rightarrow$ `Shortlisted` $\rightarrow$ `Selected`), and inspect full placement history.

### 4.4 Documentation Checkpoints
* **Vue.js Documentation:** Visit the [Vue.js Guide](https://vuejs.org/) to structure reactive components, handle data bindings (`v-model`), and manage component lifecycle hooks (`mounted()`).
* **Bootstrap Documentation:** Use [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/getting-started/introduction/) for responsive grid layouts, card components, tables, and form controls.

---

## Phase 5: Performance Optimization & Caching

### 5.1 Caching Strategy
* Integrate **Redis** to cache heavy read queries (e.g., public approved placement drive listings or aggregate admin statistics).
* Set explicit cache expiry times (TTL) so data stays fresh without putting unnecessary strain on the SQLite database.

### 5.2 Why Cache?
In placement seasons, hundreds of students might hit the portal simultaneously to check newly posted drives. Caching reduces database query latency and ensures lightning-fast API responses.

### 5.3 Documentation Checkpoints
* **Flask-Caching:** Read the official Flask-Caching extension guide for configuring Redis as a cache backend (`CACHE_TYPE = "redis"`).

---

## Phase 6: Background Jobs, Scheduling & Async Tasks

### 6.1 Configuring Celery & Redis Broker
Set up Celery with Redis acting as both the message broker and backend result store.

### 6.2 Required Background Tasks
1. **Scheduled Job - Daily Reminders (Cron/Celery Beat):**
   * Runs daily at a scheduled time.
   * Scans for upcoming application deadlines and pushes reminder alerts via Google Chat Webhooks, email, or SMS.
2. **Scheduled Job - Monthly Activity Report:**
   * Executes on the first day of every month.
   * Compiles total drives conducted, applications received, and selections made.
   * Generates an HTML report and emails it directly to the Admin.
3. **User-Triggered Async Job - Export Applications as CSV:**
   * Triggered when a student clicks "Export History" on their dashboard.
   * Asynchronously compiles student history (Student ID, Company Name, Drive Title, Status, Dates) into a CSV file and alerts the student upon completion.

### 6.3 Documentation Checkpoints
* **Celery Documentation:** Read the [First Steps with Celery Guide](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html) for setting up worker nodes and periodic tasks (`celery-beat`).
* **Flask-Mail:** Consult Flask-Mail documentation for sending automated HTML reports and notification emails.

---

## Phase 7: Testing, Video Presentation & Final Submission

### 7.1 Local Verification Checklist
* Verify that all demos run seamlessly on your local machine.
* Test edge cases: Can a student apply twice to the same drive? (Should be blocked). Can a company create a drive before approval? (Should be blocked). Is the database created purely through code?

### 7.2 Project Report & Video Preparation
* **Project Report (Max 5 pages):** Compile student details, problem statement approach, LLM/AI declaration, frameworks list, ER diagram, API endpoints, and the presentation video drive link into the official template.
* **Video Presentation (5-10 minutes):**
  1. *Introduction (30 sec)*
  2. *Approach (30 sec)*
  3. *Key Features Demonstration (90 sec)*
  4. *Additional Features (30 sec)*
  5. *Live code walkthrough and Q&A preparation.*

---

### What's Next?
Review this blueprint to ensure all framework constraints and core features are aligned. Would you like to start writing the database models in `models.py` or set up the Flask application factory first?