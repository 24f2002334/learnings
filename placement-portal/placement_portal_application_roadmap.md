# Placement Portal Application (PPA - V2)
**Project Requirements & Development Roadmap**

---

## 1. Project Overview
Institutes require efficient systems to manage campus recruitment activities involving companies and students. Currently, many institutes rely on spreadsheets, emails, or manual coordination, which makes it difficult to manage company approvals, placement drives, student registrations, and application tracking.

You are required to build a **Placement Portal Application (PPA)** web application that allows three user roles to interact with the system securely: **Admin (Institute)**, **Companies**, and **Students**.

---

## 2. Mandatory Tech Stack & Rules
* **API Framework:** Flask (Python)
* **UI Framework:** Vue.js (CDN-based entry point with Jinja2 or Vue CLI if required)
* **Styling:** Bootstrap (No other CSS framework is allowed)
* **Database:** SQLite (Must be created programmatically via code/models; manual creation like DB Browser is prohibited)
* **Caching:** Redis
* **Batch Jobs & Async Processing:** Celery + Redis
* **Constraint:** All demos must run locally. No external libraries/frameworks outside the specified list are permitted.

---

## 3. Roles & Functionalities

### A. Admin (Institute Placement Cell)
* Pre-existing superuser created programmatically on startup (no registration form for admin).
* Approve or reject company registrations.
* Approve or reject placement drives created by companies.
* View and manage all students, companies, and placement drives.
* Search for students or companies.
* Blacklist or deactivate companies and students.
* View reports and placement statistics.

### B. Company
* Register company profile.
* Create placement drives (only after Admin approval).
* View student applications for their placement drives.
* Shortlist students, schedule interviews, and update final selection results.

### C. Student
* Self-register, log in, and update profile/resume.
* View approved placement drives with eligibility-based filtering/searching.
* Apply for placement drives (prevents duplicate applications and validates eligibility).
* View application status, past placement history, and trigger a CSV export.

---

## 4. Key Terminologies & Data Entities

* **Placement Drive:** Recruitment event created by a company.
  * *Attributes:* Drive ID, Company ID, Job Title, Job Description, Eligibility Criteria (Branch, CGPA, Year), Application Deadline, Status (`Pending` / `Approved` / `Closed`).
* **Application:** Record of a student applying to a drive.
  * *Attributes:* Application ID, Student ID, Drive ID, Application Date, Status (`Applied` / `Shortlisted` / `Selected` / `Rejected`).
* **Company Profile:** Details of a registered corporate partner.
  * *Attributes:* Company ID, Company Name, HR Contact, Website, Approval Status.

---

## 5. Backend Jobs & Caching

1. **Scheduled Daily Reminders (Celery + Redis):**
   * Sends daily reminders to students regarding upcoming application deadlines via email, SMS, or Google Chat Webhooks.
2. **Scheduled Monthly Activity Report:**
   * Generates monthly placement activity reports (drives conducted, applications, selections) on the 1st of every month and emails them to the admin as HTML/PDF.
3. **User-Triggered Async Job (CSV Export):**
   * Students can export their application history as a CSV file asynchronously, receiving an alert once generated.
4. **Performance & Caching:**
   * Implement Redis caching with cache expiry on frequently requested endpoints to optimize API response times.

---

## 6. Step-by-Step Development Roadmap

### Phase 1: Environment Setup & Database Modeling
* **Step 1.1:** Initialize your Python virtual environment and install dependencies (`Flask`, `Flask-SQLAlchemy`, `Flask-Security` or `JWT`, `Celery`, `Redis`).
  * *When to refer documentation:* Flask-SQLAlchemy documentation for configuring SQLite database URIs.
* **Step 1.2:** Define database models programmatically (`User`, `Role`, `Company`, `Drive`, `Application`) using SQLAlchemy. Ensure constraints and relationships are properly set up.
  * *When to refer documentation:* SQLAlchemy relationship definitions and backrefs.
* **Step 1.3:** Write a script/hook to programmatically seed the default Admin user on app startup.

### Phase 2: Authentication & Role-Based Access Control (RBAC)
* **Step 2.1:** Implement user registration and login endpoints for Students and Companies. Implement secure password hashing.
* **Step 2.2:** Set up role-based access control protecting admin, company, and student routes using Flask session or tokens.
  * *When to refer documentation:* Flask-Security or Flask-JWT-Extended documentation for token generation and decorators.

### Phase 3: Core API Development (Flask)
* **Step 3.1:** **Admin APIs:** Endpoints for fetching pending companies/drives, approving/rejecting them, searching users, and toggling blacklist status.
* **Step 3.2:** **Company APIs:** Endpoints for profile creation, creating drives, viewing applications, and updating selection statuses.
* **Step 3.3:** **Student APIs:** Endpoints for browsing/filtering approved drives, applying for drives (with eligibility checks), and viewing personal history.
  * *When to refer documentation:* Flask RESTful routing or Blueprint design patterns.

### Phase 4: Frontend Development (Vue.js + Bootstrap)
* **Step 4.1:** Set up the main HTML entry point using Jinja2 and load Vue.js along with Bootstrap via CDN (or use Vue CLI if preferred).
* **Step 4.2:** Build reusable views/components for the Admin Dashboard, Company Dashboard, and Student Portal.
* **Step 4.3:** Implement frontend validation using HTML5/JavaScript on forms (registration, drive creation, profile edits).

### Phase 5: Caching & Background Jobs (Redis & Celery)
* **Step 5.1:** Integrate Redis caching for heavy read queries (e.g., listing approved drives) with proper cache expiry.
* **Step 5.2:** Configure Celery with Redis broker for background task execution.
* **Step 5.3:** Implement the Celery beat schedule for daily reminders and monthly report generation. Implement the student CSV export task.
  * *When to refer documentation:* Celery First Steps / Periodic Tasks documentation.

### Phase 6: Testing, Documentation, & Packaging
* **Step 6.1:** Thoroughly test end-to-end user journeys locally.
* **Step 6.2:** Prepare the project report (max 5 pages) covering student details, approach, frameworks, ER diagram, API endpoints, and AI/LLM usage declaration.
* **Step 6.3:** Record a 5-10 minute video demonstration highlighting key features and walkthrough.
* **Step 6.4:** Package all code cleanly into a single zip file as per submission instructions.