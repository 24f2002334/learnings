# you asked

message time: 2026-10-05 17:38:56

make md file from this

---

# deepseek response

# Teacher-Style Mode

## User:

can you become my teacher and turn your talking style into a teaching style

## Kimi:

Yes. I can switch into a teacher-style mode.

When you want that, tell me what you want to learn, and I'll explain it in a clear, structured way—like a teacher would: step by step, with examples, checks for understanding, and practice questions if you want.

If you'd like, I can use a style like:

- simple explanations
- patient and encouraging tone
- short lessons with summaries
- quizzes at the end
- real-life examples
- step-by-step problem solving

If you want, you can also tell me:
1. what subject you want to learn
2. your level (beginner / intermediate / advanced)
3. how you want me to teach (strict, friendly, exam-focused, casual, etc.)

Then I'll start teaching.

## Kimi:

## Kimi:

Lesson 1: Welcome to Your Placement Portal Project (PPA)

Great — I'm your teacher now, and we'll build this project together, step by step, from an empty folder to a fully working app. I'll explain what we do, why we do it, and when to check the official documentation (important — examiners love asking "where did you learn this?").

Let's begin.

### Step 0: Understand the Big Picture (Read this first)

Before touching code, you must understand what you're building and why each technology exists. This matters for your viva.

#### The architecture (draw this in your notes)

```
Browser (Vue.js + Bootstrap)
- Renders pages, forms, dashboards
        |
        | HTTP requests (JSON via AJAX)
        v
Flask API (Python)
- Authentication, business logic, validation
- Talks to DB, Redis cache
        |
        +----------------------+
        |                      |
        v                      v
SQLite (DB)                Redis + Celery
- Users                    - Caching
- Drives                   - Daily reminders
- Apps                     - Monthly reports
                           - CSV export jobs
```

#### Why each technology? (Viva question alert)

| Technology | Why it's used |
|---|---|
| Flask | Lightweight Python web framework for building REST APIs quickly |
| VueJS | Reactive frontend — updates UI without page reloads |
| Bootstrap | Pre-built responsive CSS components (allowed styling framework) |
| SQLite | Lightweight file-based DB, zero setup, perfect for local demos |
| Redis | In-memory store → very fast reads (caching), and a message broker for Celery |
| Celery | Runs background/scheduled jobs (reminders, reports) so the web app stays fast |

**Teacher's tip:** If an examiner asks "Why Redis for caching?" — answer: "SQLite disk reads are slow for repeated dashboard queries; Redis stores results in memory with an expiry time, so repeated requests are near-instant and we invalidate the cache when data changes."

### Step 1: Set Up Your Development Environment

#### 1.1 Create the project folder

```bash
mkdir placement-portal
cd placement-portal
```

#### 1.2 Create a Python virtual environment — why?

A virtual environment isolates this project's packages from your system Python, so versions never conflict (e.g., if another project needs a different Flask version).

```bash
python -m venv venv
```

Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

You'll see `(venv)` at the start of your terminal line — that means it worked.

#### 1.3 Install the required packages

```bash
pip install flask flask-sqlalchemy flask-cors flask-jwt-extended redis celery
```

What each does (know this for the report):
- `flask` — the web framework
- `flask-sqlalchemy` — ORM to create tables programmatically (the project doc REQUIRES this — no DB Browser allowed)
- `flask-cors` — lets Vue (running on a different port) talk to Flask
- `flask-jwt-extended` — JWT token authentication

#### 1.4 Install and start Redis (required!)

Windows: Redis doesn't run natively — use Docker (`docker run -p 6379:6379 redis`) or Memurai.
Mac: `brew install redis && brew services start redis`
Linux: `sudo apt install redis-server && sudo service redis-server start`

Why Redis must run first: Celery uses Redis as its message broker, and our caching needs it. If Redis is down, background jobs fail.

Test it: run `redis-cli ping` → should reply `PONG`.

### Checkpoint 1 - Do this before the next lesson

1. Create the folder, venv, and activate it
2. Install all packages successfully
3. Get Redis running and confirm PONG

Quick quiz (answer to yourself - or reply to me):
1. Why do we use a virtual environment?
2. Why can't we create the database with DB Browser for SQLite?
3. What happens if Redis isn't running when Celery tries to start?

Once you confirm you're done with Checkpoint 1, Lesson 2 will be: Designing the database models (User, Company, Drive, Application) — the foundation of everything. We'll write the code together and I'll explain the ER relationships. Tell me when you're ready, or ask questions if anything above is unclear.

## User:

yes i am ready

## Kimi:

Lesson 2: Designing the Database — The Foundation

Excellent. Now we build the heart of the application. Everything else — dashboards, applications, reports — depends on getting this right.

### Step 2.1: Plan the ER Diagram First (Never Code Blind)

A common student mistake is jumping to code. We design on paper first. Here's our design:

```
USER
id (PK)
email
password_hash
role
is_active
created_at
    |
    | 1:1 (a company IS a user)
    v
COMPANY
id (PK)
user_id (FK->User)
name
hr_contact
website
approval_status
is_blacklisted
    |
    | 1:N
    v
PLACEMENT_DRIVE
id (PK)
company_id (FK)
job_title
job_description
min_cgpa
eligible_branch
eligible_year
application_deadline
status
    |
    | 1:N
    v
APPLICATION
id (PK)
student_id (FK)
drive_id (FK)
applied_at
status

STUDENT
id (PK)
user_id (FK->User)
name
branch
cgpa
year
resume_filename
    |
    | 1:N
    v
APPLICATION (N:1)
```

#### Key design decisions — understand the WHY (viva questions)

**Q: Why one unified user table instead of separate student, company, admin tables?**
The project doc explicitly requires "a unified user model." This means: login is done once against User, and role decides what you can access. A Company and Student each have a one-to-one profile row linked via user_id.

**Q: Why a separate Application table instead of storing student IDs inside the drive?**
Because it's a many-to-many relationship (one student applies to many drives; one drive has many applicants). In databases, M:N relationships always become a junction table. This also lets us store application status per student-drive pair.

**Q: What prevents duplicate applications?**
A unique constraint on (student_id, drive_id) — enforced by the database itself, not just our code. This is more reliable.

### 2.2: Create the Project Structure

```
placement-portal/
  backend/
    app.py          entry point
    models.py       database models (today's file)
    config.py       settings
    routes/
      __init__.py
    jobs/
      __init__.py
  frontend/
  venv/
```

Create empty `__init__.py` files in `routes/` and `jobs/` folders so Python treats them as packages.

### Step 2.3: Write config.py - Why a Config File?

Hardcoding settings (like secret keys) scattered in code is bad practice. One config file = one place to change things.

```python
# backend/config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "dev-secret-change-in-production"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "placement.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # saves memory; we don't need this feature
    JWT_SECRET_KEY = "jwt-dev-secret"
    REDIS_URL = "redis://localhost:6379/0"
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
```

Docs to refer: Flask config handling →
https://flask.palletsprojects.com/config/

### Step 2.4: Write models.py - The Most Important File

```python
# backend/models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # student / company / admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_profile = db.relationship("Student", backref="user", uselist=False, lazy=True)
    company_profile = db.relationship("Company", backref="user", uselist=False, lazy=True)

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float)
    year = db.Column(db.Integer)
    resume_filename = db.Column(db.String(255))

class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    hr_contact = db.Column(db.String(120))
    website = db.Column(db.String(200))
    approval_status = db.Column(db.String(20), default="pending")  # pending/approved/rejected
    is_blacklisted = db.Column(db.Boolean, default=False)

class PlacementDrive(db.Model):
    __tablename__ = "placement_drives"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    job_title = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.Text)
    eligible_branch = db.Column(db.String(50))
    min_cgpa = db.Column(db.Float, default=0.0)
    eligible_year = db.Column(db.Integer)
    application_deadline = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending/approved/closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship("Application", backref="drive", lazy=True)

class Application(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey("placement_drives.id"), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="applied")  # applied → shortlisted → selected / rejected
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id", name="uq_student_drive"),
    )
```

#### Teacher's explanation of tricky parts

`db.relationship(...)` vs `db.ForeignKey(...)` — a classic confusion:
- **ForeignKey** = the actual column in the database that stores the link
- **relationship** = a Python convenience that lets you write `drive.applications` to get all applications without writing SQL joins manually

`uselist=False` on `student_profile` means one user → at most one student profile (enforces the 1:1).

`__table_args__` with `UniqueConstraint` — this is the database-level duplicate-application prevention we discussed. Even if our Python code has a bug, the DB will reject a second insert.

Docs to refer: relationships →
https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html

### Step 2.5: Write app.py — and Create the Admin Programmatically

```python
# backend/app.py
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # allows Vue (different port) to call our API
db.init_app(app)

def create_admin():
    """Create the single pre-existing admin - required by project doc."""
    if not User.query.filter_by(role="admin").first():
        admin = User(
            email="admin@institute.edu",
            password_hash=generate_password_hash("admin123"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created: admin@institute.edu / admin123")

with app.app_context():
    db.create_all()       # creates tables programmatically
    create_admin()        # no admin registration allowed

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

**Why `with app.app_context():`?** Flask needs an "application context" to talk to the database outside of a request. `db.create_all()` and our admin creation run at startup, not during a web request, so we need this block. (Examiners ask this.)

**Why `generate_password_hash`?** We never store plain-text passwords. If the DB leaks, attackers get hashes, not real passwords.

### Checkpoint 2 - Run It and Verify

```bash
cd backend
python app.py
```

You should see:

```
Admin created: admin@institute.edu / admin123
 * Running on http://127.0.0.1:5000
```

Then verify the database was created programmatically (do not open DB Browser to create anything - just look):

```bash
ls  # you should see placement.db appear
```

Stop the server (Ctrl+C), then run it again - this time it should NOT print the admin message. Why? Because `create_admin()` checks if an admin already exists. This proves our idempotent setup works.

### Quick Quiz (reply with answers)

1. Why do we store role in a unified User table instead of three separate tables?
2. What does the `UniqueConstraint("student_id", "drive_id")` protect against, and why is DB-level better than Python-level?
3. What's the difference between `db.ForeignKey` and `db.relationship`?
4. What does `uselist=False` do?
5. Why does `create_admin()` run inside `app.app_context()`?

Next lesson - Lesson 3: Authentication API (register/login with JWT tokens for all three roles). This is where students most often get stuck, so we'll go slowly with Postman testing at each step.

Reply with your quiz answers (or just "done + ready") and we'll continue.

## User:

done + ready

## Kimi:

Lesson 3: Authentication — Register, Login, and JWT Tokens

Great. Today we build the security layer — the most commonly asked-about part in vivas. We'll build it slowly and test every endpoint before moving on.

### Step 3.1: Understand the Auth Flow First (Concept Before Code)

How JWT works — and why we chose it (viva question)

When a user logs in, the server creates a token (a long string) containing the user's identity + role, signed with a secret key. The client (Vue app) stores it and sends it with every request:

1. `POST /api/login {email, password}`
2. Server verifies password → creates JWT → sends it back
3. Client stores token (localStorage), sends in header: `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`
4. Server decodes & verifies token on every protected route

Why JWT instead of sessions? The project doc allows both. JWT is stateless — the server doesn't store session data; everything needed is inside the token. This scales better and is the modern standard for API-first apps (which ours is — Flask API + Vue frontend are separate).

Docs: https://flask-jwt-extended.readthedocs.io/en/stable/basic_usage.html

### Step 3.2: Create routes/auth.py — Register & Login

Create the file `backend/routes/auth.py`:

```python
# backend/routes/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Student, Company

auth_bp = Blueprint("auth", __name__, url_prefix="/api")

@auth_bp.post("/register/student")
def register_student():
    data = request.get_json()
    # --- Backend validation (required by project doc) ---
    if not data.get("email") or not data.get("password") or not data.get("name"):
        return jsonify({"error": "email, password and name are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already registered"}), 409

    # --- Create unified user + student profile ---
    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="student",
    )
    db.session.add(user)
    db.session.flush()  # assigns user.id without full commit

    student = Student(
        user_id=user.id,
        name=data["name"],
        branch=data.get("branch"),
        cgpa=data.get("cgpa"),
        year=data.get("year"),
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "student registered"}), 201

@auth_bp.post("/register/company")
def register_company():
    data = request.get_json()
    if not data.get("email") or not data.get("password") or not data.get("name"):
        return jsonify({"error": "email, password and name are required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        role="company",
    )
    db.session.add(user)
    db.session.flush()

    company = Company(
        user_id=user.id,
        name=data["name"],
        hr_contact=data.get("hr_contact"),
        website=data.get("website"),
        approval_status="pending",  # admin must approve before any activity
    )
    db.session.add(company)
    db.session.commit()
    return jsonify({"message": "company registered, awaiting admin approval"}), 201

@auth_bp.post("/login")
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    # Same error message for both cases → doesn't reveal which one was wrong
    if not user or not check_password_hash(user.password_hash, data.get("password", "")):
        return jsonify({"error": "invalid email or password"}), 401

    if not user.is_active:
        return jsonify({"error": "account deactivated"}), 403

    # Block unapproved companies
    if user.role == "company":
        company = user.company_profile
        if company.is_blacklisted:
            return jsonify({"error": "company is blacklisted"}), 403
        if company.approval_status != "approved":
            return jsonify({"error": "company not yet approved by admin"}), 403

    # --- The JWT token carries role inside - used for access control ---
    token = create_access_token(identity=user.id, additional_claims={"role": user.role})

    return jsonify({
        "token": token,
        "role": user.role,
    }), 200
```

#### Teacher's explanation of tricky parts

**Why `db.session.flush()` instead of `commit()`?** `flush()` sends the INSERT to the database so `user.id` gets generated, but doesn't make it permanent yet. Then we create the profile with that `user_id`, and one `commit()` saves both. Two separate commits could leave orphaned data if the second fails.

**Why the same error message for "wrong email" and "wrong password"?** Security. If an attacker gets "wrong password," they now know the email exists and can focus on cracking just the password. Always respond identically.

**`additional_claims={"role": user.role}`** - this embeds the role inside the signed token. The server can trust it because tampering would break the signature. This is how we'll do role-based access control in the next lesson.

Note there is no `/register/admin` route at all. The project doc forbids admin registration - our admin exists only because `create_admin()` made it programmatically.

### Step 3.3: Wire It Into app.py

Update `backend/app.py`:

```python
# backend/app.py (updated)
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from models import db, User
from werkzeug.security import generate_password_hash
from routes.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
jwt = JWTManager(app)  # new: enables token verification
app.register_blueprint(auth_bp)  # new: adds our auth routes

def create_admin():
    if not User.query.filter_by(role="admin").first():
        admin = User(
            email="admin@institute.edu",
            password_hash=generate_password_hash("admin123"),
            role="admin",
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin created")

with app.app_context():
    db.create_all()
    create_admin()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
```

**Why Blueprints?** They organize routes into modules. Later we'll have `routes/admin.py`, `routes/student.py`, etc. — each registers as its own blueprint. Keeps files small and focused.

### Step 3.4: Test Everything with curl (Before Building Any UI)

Start the server (`python app.py`), open a second terminal, and run:

#### Test 1 - Register a student:

```bash
curl -X POST http://127.0.0.1:5000/api/register/student \
  -H "Content-Type: application/json" \
  -d '{"email":"priya@student.edu","password":"pass123","name":"Priya","branch":"CSE","cgpa":"8.5","year":"4"}'
```

Expected: `{"message":"student registered"}` with status 201.

#### Test 2 - Register a company:

```bash
curl -X POST http://127.0.0.1:5000/api/register/company \
  -H "Content-Type: application/json" \
  -d '{"email":"hr@techcorp.com","password":"pass123","name":"TechCorp","hr_contact":"hr@techcorp.com","website":"https://techcorp.com"}'
```

#### Test 3 - Try logging in as the company (should be BLOCKED - not approved yet):

```bash
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"hr@techcorp.com","password":"pass123"}'
```

Expected: `{"error":"company not yet approved by admin"}` - this proves our approval gate works!

#### Test 4 - Login as the student (should work):

```bash
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"priya@student.edu","password":"pass123"}'
```

Expected: `{"token":"eyJ...","role":"student"}` - save this token, we need it next lesson.

#### Test 5 - Negative test: wrong password (should give generic 401):

```bash
curl -X POST http://127.0.0.1:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"priya@student.edu","password":"wrong"}'
```

**Teacher's tip:** Download Postman or use the Thunderbird/REST Client extension in VS Code for testing - curl gets tedious with long tokens. Examiners are also impressed when you demo with Postman.

### Checkpoint 3

- All 5 curl tests above pass with expected results
- You have a student token saved somewhere
- You can explain why the company login was blocked

### Quick Quiz (reply with answers)

1. What is inside a JWT token, and why can the server trust the role claim inside it?
2. Why do we return the same error for "user not found" and "wrong password"?
3. What does `db.session.flush()` do, and why use it instead of `commit()` when creating user + profile?
4. Why is there no `/register/admin` endpoint?

Next lesson — Lesson 4: Role-Based Access Control. We'll build a decorator that reads the role from the JWT and blocks unauthorized access — then build the Admin endpoints (approve companies, approve drives, dashboard counts, search).

Reply with quiz answers or "done + ready"

## User:

done + ready

## Kimi:

Lesson 4: Role-Based Access Control + Admin Endpoints

Great. Today we build two things that go together: the gatekeeper (role-checking) and the Admin's toolkit (approvals, dashboard, search, blacklisting).

### Step 4.1: Build the Role-Checking Decorator (The Gatekeeper)

Right now, any logged-in user could call any endpoint. We need to check both things on every protected route:
1. Is the request carrying a valid token? (authentication)
2. Does the token's role allow this route? (authorization)

Create `backend/utils.py`:

```python
# backend/utils.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request

def role_required(*allowed_roles):
    """
    Decorator factory: allows only users whose JWT 'role' claim is in allowed_roles.
    Usage: @role_required('admin')
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # 1. reject if no/invalid token
            claims = get_jwt()       # 2. read the token's payload
            if claims.get("role") not in allowed_roles:
                return jsonify({"error": "forbidden: insufficient role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
```

#### Teacher's explanation — this is a viva favorite

**What is a decorator?** A function that wraps another function to add behavior. `@role_required("admin")` above `def dashboard()` means: every call to `dashboard()` first passes through our wrapper. Think of it like a security checkpoint before entering a room.

**Why `verify_jwt_in_request()` manually?** Normally `@jwt_required()` does this — but we need the claims first, so we call it inside our wrapper. One decorator now does both jobs: validates the token and checks the role.

**Why `functools.wraps`?** Without it, the wrapped function loses its name/docstring, which breaks Flask's URL routing and debugging. A small detail that separates polished code from student code.

Docs: custom decorators → https://flask.palletsprojects.com/patterns/viewdecorators/

### Step 4.2: Admin Endpoints — routes/admin.py

Create `backend/routes/admin.py`:

```python
# backend/routes/admin.py
from flask import Blueprint, request, jsonify
from models import db, User, Student, Company, PlacementDrive, Application
from utils import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

# --- Dashboard counts ---
@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard():
    return jsonify({
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "total_drives": PlacementDrive.query.count(),
        "pending_companies": Company.query.filter_by(approval_status="pending").count(),
        "pending_drives": PlacementDrive.query.filter_by(status="pending").count(),
    })

# --- Company approval ---
@admin_bp.get("/companies")
@role_required("admin")
def list_companies():
    q = request.args.get("q", "").strip()
    query = Company.query
    if q:
        query = query.filter(Company.name.ilike(f"%{q}%"))
    companies = query.all()
    return jsonify([{
        "id": c.id, "name": c.name, "website": c.website,
        "hr_contact": c.hr_contact, "approval_status": c.approval_status,
        "is_blacklisted": c.is_blacklisted,
    } for c in companies])

@admin_bp.post("/companies/<int:company_id>/approve")
@role_required("admin")
def approve_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = "approved"
    db.session.commit()
    return jsonify({"message": f"{company.name} approved"})

@admin_bp.post("/companies/<int:company_id>/reject")
@role_required("admin")
def reject_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.approval_status = "rejected"
    db.session.commit()
    return jsonify({"message": f"{company.name} rejected"})

@admin_bp.post("/companies/<int:company_id>/blacklist")
@role_required("admin")
def blacklist_company(company_id):
    company = Company.query.get_or_404(company_id)
    company.is_blacklisted = not company.is_blacklisted  # toggle
    db.session.commit()
    state = "blacklisted" if company.is_blacklisted else "un-blacklisted"
    return jsonify({"message": f"{company.name} {state}"})

# --- Drive approval ---
@admin_bp.get("/drives")
@role_required("admin")
def list_drives():
    q = request.args.get("q", "").strip()
    query = PlacementDrive.query
    if q:
        query = query.filter(PlacementDrive.job_title.ilike(f"%{q}%"))
    drives = query.all()
    return jsonify([{
        "id": d.id, "job_title": d.job_title, "status": d.status,
        "company": d.company.name if d.company else None,
        "deadline": d.application_deadline.isoformat(),
    } for d in drives])

@admin_bp.post("/drives/<int:drive_id>/approve")
@role_required("admin")
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "approved"
    db.session.commit()
    return jsonify({"message": f"Drive '{drive.job_title}' approved"})

@admin_bp.post("/drives/<int:drive_id>/reject")
@role_required("admin")
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = "rejected"
    db.session.commit()
    return jsonify({"message": f"Drive '{drive.job_title}' rejected"})

# --- Student management ---
@admin_bp.get("/students")
@role_required("admin")
def list_students():
    q = request.args.get("q", "").strip()
    query = Student.query
    if q:
        query = query.filter(Student.name.ilike(f"%{q}%"))
    students = query.all()
    return jsonify([{
        "id": s.id, "name": s.name, "branch": s.branch,
        "cgpa": s.cgpa, "year": s.year,
        "is_active": s.user.is_active,
    } for s in students])

@admin_bp.post("/students/<int:user_id>/deactivate")
@role_required("admin")
def deactivate_student(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    state = "deactivated" if not user.is_active else "reactivated"
    return jsonify({"message": f"student {state}"})
```

#### Teacher's explanation of decisions

- `get_or_404` — SQLAlchemy shortcut: fetches the row or automatically returns a 404 error. Cleaner than manual `if not company: return ...` every time.
- `ilike(f"%{q}%")` — case-insensitive partial matching. `ilike` (the i) means "Iron" matches "iron" too. This powers the search requirement in the project doc.
- **Blacklist/deactivate uses toggle logic** — one endpoint both blacklists and un-blacklists. Fewer endpoints, simpler UI. Note blacklist is on Company, deactivation is on User — because login checks `user.is_active` for everyone, while blacklisting is company-specific per the doc.
- `d.company.name` — this works because of the `backref="company"` relationship we defined in Lesson 2's PlacementDrive model. SQLAlchemy auto-joins; no manual SQL needed.

### Step 4.3: Register the Blueprint

Add to `app.py`:

```python
from routes.admin import admin_bp
app.register_blueprint(admin_bp)
```

### 4.4: Test the Whole Approval Flow (This is a Demo-Worthy Sequence)

In Postman (or curl), first login as admin to get an admin token:

```
POST /api/login
{email: "admin@institute.edu", password: "admin123"}
```

Then set Postman's Authorization → Bearer Token field with that token. Every request below sends it automatically.

#### Test 1 - Dashboard:

```
GET /api/admin/dashboard
```

Expected: counts including `pending_companies: 1` (your TechCorp from last lesson).

#### Test 2 - Search companies:

```
GET /api/admin/companies?q=tech
```

#### Test 3 - Approve the company:

```
POST /api/admin/companies/1/approve
```

(Use the actual ID from Test 2's response.)

#### Test 4 - Verify the gate is open:

Now login as `hr@techcorp.com` again - it should succeed this time! This proves the full approve-login chain works.

#### Test 5 - Negative test (important for demo!):

Try `GET /api/admin/dashboard` with the student token from Lesson 3. Expected: `403 forbidden: insufficient role`. This proves role-based access control works. Examiners love when you demonstrate a 403 live.

#### Test 6 - Try with no token at all:

Same endpoint, no Authorization header → `401 error`.

Different from 403 - know the difference:
- **401 Unauthorized** = "who are you?" (no/invalid token)
- **403 Forbidden** = "I know who you are, but you're not allowed" (wrong role)

### Checkpoint 4

- Admin dashboard returns counts
- Company approval works, and the company can then log in
- Student token gets 403 on admin routes
- No token gets 401

### Quick Quiz (reply with answers)

1. What's the difference between 401 and 403? Give a real example from our app.
2. Why do we need `verify_jwt_in_request()` inside our decorator instead of just reading the header manually?
3. Why does `d.company.name` work without writing a SQL JOIN?
4. What does `ilike("%tech%")` match — and why `ilike` instead of `like`?

Next lesson — Lesson 5: Company endpoints (create drives, view applicants, shortlist) and Student endpoints (browse approved drives, eligibility validation, apply exactly once). This is the core business logic of the whole app.

Reply with quiz answers or "done + ready"

## User:

done + ready

## Kimi:

Lesson 5: The Core Business Logic — Drives & Applications

This is the heart of the app. Everything the project doc cares most about happens here: companies creating drives, students applying with eligibility validation, and status updates flowing through the pipeline.

### Step 5.1: Get the Current User's Identity from the Token

Both companies and students need to know "who is calling?" from their token. Add this helper to `utils.py`:

```python
# add to backend/utils.py
from flask_jwt_extended import get_jwt_identity

def current_user_id():
    """Returns the user.id stored in the JWT token."""
    return get_jwt_identity()
```

Then add a convenience to fetch profiles in `models.py`... actually, simpler: we query directly in routes. But first — add one relationship we're missing. In `models.py`, add `company` relationship to PlacementDrive and `student` to Application if not present:

```python
# PlacementDrive - add this line inside the class:
company = db.relationship("Company", backref="drives", lazy=True)

# Application - add these:
student = db.relationship("Student", backref="applications", lazy=True)
```

**Why now?** `d.company.name` already worked via backref, but having both directions (`company.drives`, `student.applications`) makes our new code much cleaner. Delete `placement.db` and rerun `python app.py` — SQLAlchemy will recreate the schema.

### Step 5.2: Company Endpoints — routes/company.py

```python
# backend/routes/company.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Company, PlacementDrive, Application, Student
from utils import role_required, current_user_id

company_bp = Blueprint("company", __name__, url_prefix="/api/company")

def get_my_company():
    return Company.query.filter_by(user_id=current_user_id()).first_or_404()

# --- Dashboard ---
@company_bp.get("/dashboard")
@role_required("company")
def dashboard():
    company = get_my_company()
    return jsonify({
        "company": {
            "name": company.name,
            "website": company.website,
            "approval_status": company.approval_status,
        },
        "drives": [{
            "id": d.id,
            "job_title": d.job_title,
            "status": d.status,
            "deadline": d.application_deadline.isoformat(),
            "applicant_count": len(d.applications),
        } for d in company.drives],
    })

# --- Create a drive (company must be approved) ---
@company_bp.post("/drives")
@role_required("company")
def create_drive():
    company = get_my_company()
    if company.approval_status != "approved":
        return jsonify({"error": "company not approved yet"}), 403

    data = request.get_json()
    required = ["job_title", "application_deadline"]
    if not all(data.get(f) for f in required):
        return jsonify({"error": "job_title and application_deadline are required"}), 400

    try:
        deadline = datetime.fromisoformat(data["application_deadline"])
    except ValueError:
        return jsonify({"error": "deadline must be ISO format, e.g. 2026-12-01T23:59:00"}), 400

    if deadline < datetime.utcnow():
        return jsonify({"error": "deadline cannot be in the past"}), 400

    drive = PlacementDrive(
        company_id=company.id,
        job_title=data["job_title"],
        job_description=data.get("job_description"),
        eligible_branch=data.get("eligible_branch"),
        min_cgpa=float(data.get("min_cgpa", 0)),
        eligible_year=int(data["eligible_year"]) if data.get("eligible_year") else None,
        application_deadline=deadline,
        status="pending",  # admin must approve before students see it
    )
    db.session.add(drive)
    db.session.commit()
    return jsonify({"message": "drive created, awaiting admin approval", "id": drive.id}), 201

# --- View applicants for a drive ---
@company_bp.get("/drives/<int:drive_id>/applications")
@role_required("company")
def view_applications(drive_id):
    company = get_my_company()
    drive = PlacementDrive.query.get_or_404(drive_id)

    # Ownership check: companies can only see THEIR OWN drives
    if drive.company_id != company.id:
        return jsonify({"error": "not your drive"}), 403

    apps = Application.query.filter_by(drive_id=drive.id).all()
    return jsonify([{
        "application_id": a.id,
        "student": {
            "id": a.student.id, "name": a.student.name,
            "branch": a.student.branch, "cgpa": a.student.cgpa,
            "year": a.student.year,
        },
        "applied_at": a.applied_at.isoformat(),
        "status": a.status,
    } for a in apps])

# --- Update application status (shortlist / select / reject) ---
@company_bp.post("/applications/<int:app_id>/status")
@role_required("company")
def update_status(app_id):
    application = Application.query.get_or_404(app_id)
    company = get_my_company()

    # Can only touch applications for own drives
    if application.drive.company_id != company.id:
        return jsonify({"error": "not your application"}), 403

    valid = ["applied", "shortlisted", "selected", "rejected"]
    new_status = request.get_json().get("status", "").lower()
    if new_status not in valid:
        return jsonify({"error": f"status must be one of {valid}"}), 400

    application.status = new_status
    db.session.commit()
    return jsonify({"message": f"application marked {new_status}"})
```

#### Viva-critical: The Ownership Check

Notice every route calls `get_my_company()` and compares IDs. **Never trust the URL.** A malicious company could request `/api/company/drives/5/applications` for someone else's drive. Without the check `if drive.company_id != company.id`, they'd see all applicants. This is called **Insecure Direct Object Reference (IDOR)** — a famous security flaw. Mentioning "we prevented IDOR" in your viva = instant credibility.

### Step 5.3: Student Endpoints — routes/student.py

```python
# backend/routes/student.py
from flask import Blueprint, request, jsonify
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from models import db, Student, PlacementDrive, Application
from utils import role_required, current_user_id

student_bp = Blueprint("student", __name__, url_prefix="/api/student")

def get_my_student():
    return Student.query.filter_by(user_id=current_user_id()).first_or_404()

# --- Browse APPROVED, OPEN drives + search ---
@student_bp.get("/drives")
@role_required("student")
def browse_drives():
    q = request.args.get("q", "").strip()
    now = datetime.utcnow()

    query = PlacementDrive.query.filter(
        PlacementDrive.status == "approved",
        PlacementDrive.application_deadline >= now,
    )
    if q:
        query = query.filter(PlacementDrive.job_title.ilike(f"%{q}%"))

    return jsonify([{
        "id": d.id,
        "job_title": d.job_title,
        "company": d.company.name if d.company else None,
        "eligible_branch": d.eligible_branch,
        "min_cgpa": d.min_cgpa,
        "eligible_year": d.eligible_year,
        "application_deadline": d.application_deadline.isoformat(),
    } for d in query.all()])

# --- Apply to a drive (with eligibility validation) ---
@student_bp.post("/drives/<int:drive_id>/apply")
@role_required("student")
def apply_to_drive(drive_id):
    student = get_my_student()
    drive = PlacementDrive.query.get_or_404(drive_id)

    # Only approved and still-open drives
    if drive.status != "approved":
        return jsonify({"error": "drive not open for applications"}), 403
    if drive.application_deadline < datetime.utcnow():
        return jsonify({"error": "deadline has passed"}), 403

    # --- Eligibility validation (server-side, cannot be bypassed) ---
    if drive.eligible_branch and student.branch != drive.eligible_branch:
        return jsonify({"error": "not eligible: branch mismatch"}), 403
    if student.cgpa is not None and student.cgpa < drive.min_cgpa:
        return jsonify({"error": "not eligible: CGPA below minimum"}), 403
    if drive.eligible_year and student.year != drive.eligible_year:
        return jsonify({"error": "not eligible: year mismatch"}), 403

    # --- Duplicate check (Python level - fast feedback) ---
    existing = Application.query.filter_by(
        student_id=student.id, drive_id=drive.id).first()
    if existing:
        return jsonify({"error": "already applied to this drive"}), 409

    application = Application(student_id=student.id, drive_id=drive.id)
    try:
        db.session.add(application)
        db.session.commit()
    except IntegrityError:
        # Race-condition safety: UniqueConstraint fires if two requests
        # arrived at the exact same moment
        db.session.rollback()
        return jsonify({"error": "already applied to this drive"}), 409

    return jsonify({"message": "application submitted", "id": application.id}), 201

# --- My applications (status + history) ---
@student_bp.get("/applications")
@role_required("student")
def my_applications():
    student = get_my_student()
    apps = Application.query.filter_by(student_id=student.id) \
        .order_by(Application.applied_at.desc()).all()
    return jsonify([{
        "id": a.id,
        "company": a.drive.company.name,
        "drive_title": a.drive.job_title,
        "status": a.status,
        "applied_at": a.applied_at.isoformat(),
    } for a in apps])

# --- Edit profile ---
@student_bp.put("/profile")
@role_required("student")
def edit_profile():
    student = get_my_student()
    data = request.get_json()
    for field in ["name", "branch", "cgpa", "year"]:
        if field in data:
            setattr(student, field, data[field])
    db.session.commit()
    return jsonify({"message": "profile updated"})
```

#### Viva-critical: Why the Check-Both-Levels Pattern?

We check duplicates twice: once in Python (`existing = ...`) and once at the DB (`UniqueConstraint` + `IntegrityError` catch). Why? Imagine two clicks at the exact same millisecond. Both Python checks pass (neither sees the other's insert yet) — but the DB constraint catches the loser.

This is called a **race condition**, and handling it is senior-level detail. The project doc explicitly says "prevent students from applying multiple times" — this pattern is the correct answer.

Also notice: we check eligibility **before** inserting. "Validate first, write second" is the golden rule of backend validation.

### Step 5.4: Register Blueprints & Test

Add to `app.py`:

```python
from routes.company import company_bp
from routes.student import student_bp
app.register_blueprint(company_bp)
app.register_blueprint(student_bp)
```

#### Full End-to-End Test Sequence (this exact flow will wow your examiner)

| # | Actor | Action | Expected |
|---|---|---|---|
| 1 | Company | POST /api/company/drives | 201, status pending |
| 2 | Student | GET /api/student/drives | Drive NOT visible (not approved) |
| 3 | Admin | POST /api/admin/drives/1/approve | approved |
| 4 | Student | GET /api/student/drives | Drive now visible |
| 5 | Student | POST /api/student/drives/1/apply (ineligible CGPA) | 403 with reason |
| 6 | Student | fix profile CGPA, apply again | 201 |
| 7 | Student | apply again | 409 duplicate |
| 8 | Company | GET /api/company/drives/1/applications | sees Priya |
| 9 | Company | POST /api/company/applications/1/status {status: "shortlisted"} | ok |
| 10 | Student | GET /api/student/applications | sees shortlisted |

Test 2 is the subtle one students forget — unapproved drives must be invisible to students. Point 5 in your demo and say "eligibility is enforced server-side, so it can't be bypassed by the browser."

### Checkpoint 5

- All 10 test steps pass
- You demonstrated a 409 duplicate and a 403 ineligible application
- You can explain why we check both Python-level AND DB-level for duplicates

### Quick Quiz (reply with answers)

1. What is IDOR, and which lines of code prevent it in our app?
2. Why is the Python duplicate check alone not enough? What attacks the remaining gap?
3. Why does the student drive list filter on `status == "approved"` AND deadline?
4. A company is approved but tries to create a drive — what stops them if not approved? Which field guards this?

Next lesson — Lesson 6: The frontend! We finally build the Vue.js + Bootstrap UI that talks to everything we made. I'll show you the Vue-CDN architecture (no build step needed), how to store the JWT token, route between pages, and build the Student dashboard first.

Reply with quiz answers or "done + ready"

## User:

done + ready

## Kimi:

Lesson 6: The Frontend — Vue.js + Bootstrap UI

Excellent. Backend is solid. Now we build what the user actually sees. This lesson has a lot of code — go piece by piece.

### Step 6.1: Frontend Architecture — Understanding the Constraint

The project doc says: "Jinja2 templates if using CDN only for entry point (not to be used for UI)."

What this means: Flask serves **one** HTML file (the entry point). Everything else is Vue.js doing AJAX calls to our API. We use Vue via CDN — no npm, no build step, no CLI. This is the simplest approach and fully compliant.

```
Browser loads:
  GET / → Flask renders index.html (Jinja2, just for this one file)
         contains Vue + Bootstrap from CDN
Vue takes over. All page switching = show/hide divs.
All data = fetch() calls to /api/* with the JWT token.
```

#### How "routing" works without a router

We won't use Vue Router (keeps it simple and dependency-free). Instead: a `currentPage` data variable, and every "page" is a `<div v-if="currentPage == 'login'">`. Clicking a button just changes the variable. Simple, works, and easy to explain in a viva.

Docs to refer: Vue via CDN → https://vuejs.org/guide/quick-start.html#using-vue-from-cdn

### Step 6.2: Serve the Entry Point from Flask

Update `app.py` - add at the top of the imports: `from flask import render_template`

And add the route before `if __name__`:

```python
@app.get("/")
def index():
    return render_template("index.html")
```

### Step 6.3: The Directory + Entry Point

Create `backend/templates/index.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Placement Portal</title>
    <!-- Bootstrap 5 (the ONLY allowed CSS framework) -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Vue 3 from CDN -->
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
</head>
<body>
<div id="app" class="container py-4" style="max-width: 900px;">

    <!-- LOGIN / REGISTER PAGE -->
    <div v-if="page == 'login'">
        <h2 class="mb-4 text-center">Placement Portal</h2>
        <div class="card shadow-sm mx-auto" style="max-width: 450px;">
            <div class="card-body">
                <ul class="nav nav-tabs mb-3">
                    <li class="nav-item"><a class="nav-link" :class="{active: tab == 'login'}" href="#" @click.prevent="tab='login'">Login</a></li>
                    <li class="nav-item"><a class="nav-link" :class="{active: tab == 'student'}" href="#" @click.prevent="tab='student'">Student Reg</a></li>
                    <li class="nav-item"><a class="nav-link" :class="{active: tab == 'company'}" href="#" @click.prevent="tab='company'">Company Reg</a></li>
                </ul>

                <!-- Login form -->
                <div v-if="tab==='login'">
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" v-model="loginForm.email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="loginForm.password" required>
                    </div>
                    <button class="btn btn-primary w-100" @click="doLogin">Login</button>
                </div>

                <!-- student registration -->
                <div v-if="tab==='student'">
                    <div class="mb-3">
                        <label class="form-label">Name</label>
                        <input class="form-control" v-model="regStudent.name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" v-model="regStudent.email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="regStudent.password" minlength="6" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Branch</label>
                        <input class="form-control" v-model="regStudent.branch">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">CGPA</label>
                        <input type="number" step="0.01" min="0" max="10" class="form-control" v-model="regStudent.cgpa">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Year</label>
                        <input type="number" min="1" max="4" class="form-control" v-model="regStudent.year">
                    </div>
                    <button class="btn btn-success w-100" @click="registerStudent">Register</button>
                </div>

                <!-- company registration -->
                <div v-if="tab==='company'">
                    <div class="mb-3">
                        <label class="form-label">Company Name</label>
                        <input class="form-control" v-model="regCompany.name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input type="email" class="form-control" v-model="regCompany.email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="regCompany.password" minlength="6" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label">HR Contact</label>
                        <input class="form-control" v-model="regCompany.hr_contact">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Website</label>
                        <input type="url" class="form-control" v-model="regCompany.website">
                    </div>
                    <button class="btn btn-success w-100" @click="registerCompany">Register</button>
                </div>

                <div v-if="message" class="alert mt-3" :class="messageType">{{ message }}</div>
            </div>
        </div>
    </div>

    <!-- STUDENT DASHBOARD -->
    <div v-if="page == 'student'">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3>Student Dashboard</h3>
            <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
        </div>

        <div class="card mb-4 shadow-sm">
            <div class="card-body">
                <h5>Open Placement Drives</h5>
                <input class="form-control mb-3" placeholder="Search by job title..." v-model="driveSearch" @input="loadDrives">
                <ul class="list-group">
                    <li v-for="d in drives" :key="d.id" class="list-group-item d-flex justify-content-between align-items-center">
                        <div>
                            <strong>{{ d.job_title }}</strong> — {{ d.company }}
                            <br><small class="text-muted">
                                {{ d.eligible_branch || 'All branches' }} ·
                                CGPA ≥ {{ d.min_cgpa }} ·
                                Deadline: {{ d.application_deadline.slice(0,10) }}
                            </small>
                        </div>
                        <button class="btn btn-primary btn-sm" @click="applyToDrive(d.id)">Apply</button>
                    </li>
                    <li v-if="drives.length === 0" class="list-group-item text-muted">No drives found.</li>
                </ul>
            </div>
        </div>

        <!-- my applications -->
        <div class="card shadow-sm">
            <div class="card-body">
                <h5>My Applications</h5>
                <table class="table table-striped">
                    <thead><tr><th>Company</th><th>Drive</th><th>Status</th><th>Applied On</th></tr></thead>
                    <tbody>
                        <tr v-for="a in applications" :key="a.id">
                            <td>{{ a.company }}</td>
                            <td>{{ a.drive_title }}</td>
                            <td><span class="badge" :class="statusBadge(a.status)">{{ a.status }}</span></td>
                            <td>{{ a.applied_at.slice(0,10) }}</td>
                        </tr>
                    </tbody>
                </table>
                <button class="btn btn-outline-secondary" @click="exportCsv">Export as CSV</button>
            </div>
        </div>
        <div v-if="message" class="alert mt-3" :class="messageType">{{ message }}</div>
    </div>

    <!-- company & admin dashboards: Lesson 7 -->
    <div v-if="page === 'company'"><h3>Company Dashboard — coming in Lesson 7</h3></div>
    <div v-if="page === 'admin'"><h3>Admin Dashboard — coming in Lesson 7</h3></div>

</div>
<script src="/static/app.js"></script>
</body>
</html>
```

### Step 6.4: The Vue App — backend/static/app.js

Create the folder `backend/static/` and file `app.js`:

```javascript
const { createApp } = Vue;

createApp({
    data() {
        return {
            page: 'login',
            tab: 'login',
            message: '',
            messageType: 'alert-info',
            loginForm: { email: '', password: '' },
            regStudent: { name: '', email: '', password: '', branch: '', cgpa: '', year: '' },
            regCompany: { name: '', email: '', password: '', hr_contact: '', website: '' },
            drives: [],
            applications: [],
            driveSearch: '',
        };
    },
    methods: {
        // --- THE most important helper: every API call sends the token ---
        async api(url, options = {}) {
            const token = localStorage.getItem('token');
            const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
            if (token) headers['Authorization'] = 'Bearer ' + token;
            const res = await fetch(url, { ...options, headers });
            const data = await res.json().catch(() => ({}));
            if (!res.ok) throw new Error(data.error || ('HTTP ' + res.status));
            return data;
        },
        notify(msg, isError = false) {
            this.message = msg;
            this.messageType = isError ? 'alert-danger' : 'alert-success';
            setTimeout(() => { this.message = ''; }, 4000);
        },
        async doLogin() {
            try {
                const data = await this.api('/api/login', {
                    method: 'POST',
                    body: JSON.stringify(this.loginForm),
                });
                // store token - survives page refresh
                localStorage.setItem('token', data.token);
                localStorage.setItem('role', data.role);
                if (data.role === 'student') {
                    this.page = 'student'; this.loadDrives(); this.loadApplications();
                } else if (data.role === 'company') {
                    this.page = 'company';
                } else {
                    this.page = 'admin';
                }
            } catch (e) {
                this.notify(e.message, true);
            }
        },
        async registerStudent() {
            try {
                await this.api('/api/register/student', {
                    method: 'POST', body: JSON.stringify(this.regStudent),
                });
                this.notify('Registered! Please log in.');
                this.tab = 'login';
            } catch (e) {
                this.notify(e.message, true);
            }
        },
        async registerCompany() {
            try {
                await this.api('/api/register/company', {
                    method: 'POST', body: JSON.stringify(this.regCompany),
                });
                this.notify('Registered! Await admin approval before logging in.');
                this.tab = 'login';
            } catch (e) {
                this.notify(e.message, true);
            }
        },
        async loadDrives() {
            try {
                const url = '/api/student/drives' + (this.driveSearch ? '?q=' + encodeURIComponent(this.driveSearch) : '');
                this.drives = await this.api(url);
            } catch (e) {
                this.notify(e.message, true);
            }
        },
        async applyToDrive(driveId) {
            try {
                await this.api(`/api/student/drives/${driveId}/apply`, { method: 'POST' });
                this.notify('Applied successfully!');
                this.loadApplications();
            } catch (e) {
                this.notify(e.message, true); // shows "already applied" etc.
            }
        },
        async loadApplications() {
            try {
                this.applications = await this.api('/api/student/applications');
            } catch (e) {
                this.notify(e.message, true);
            }
        },
        async exportCsv() {
            // Step 1: ask backend to START the job (Lesson 8 wires Celery)
            try {
                const data = await this.api('/api/student/export-csv', { method: 'POST' });
                this.notify('Export started - task ' + data.task_id);
            } catch (e) {
                this.notify(e.message, true);
            }
        },
        statusBadge(status) {
            return {
                applied: 'bg-secondary',
                shortlisted: 'bg-warning text-dark',
                selected: 'bg-success',
                rejected: 'bg-danger',
            }[status] || 'bg-secondary';
        },
        logout() {
            localStorage.removeItem('token');
            localStorage.removeItem('role');
            this.page = 'login';
        },
    },
    mounted() {
        // If the user refreshed the page, restore their session
        const token = localStorage.getItem('token');
        const role = localStorage.getItem('role');
        if (token && role) {
            this.page = role;
            if (role === 'student') { this.loadDrives(); this.loadApplications(); }
        }
    },
}).mount('#app');
```

#### Teacher's explanation of the key ideas

**Why localStorage for the token?** The token must survive page refreshes. localStorage persists in the browser. (For a real production app you'd consider httpOnly cookies for XSS safety — mention this in viva if asked; it shows depth. For this project, localStorage is standard and fine.)

**Why the `api()` helper?** Every single request needs the same two things: JSON headers and the Bearer token. One helper = zero forgotten tokens, and errors are handled in one place. Notice how `applyToDrive` just does `catch → notify(e.message)` — the backend's error text ("already applied to this drive") flows straight to the UI. The backend is the source of truth for errors; the frontend just displays them.

**Why `@input="loadDrives"` on the search box?** Debounced live search would be nicer, but this simple version reflects on every keystroke — good enough and easy to explain. (Viva tip: "in production I'd debounce this to avoid hammering the API.")

**v-model — two-way binding:** typing in the input updates the JS variable automatically. No getElementById, no manual event listeners. This is Vue's core magic.

### Step 6.5: One Small Backend Addition for the CSV Button

Our button calls `/api/student/export-csv` which doesn't exist yet. For now, add a stub in `routes/student.py` (we'll make it truly async in Lesson 8):

```python
@student_bp.post("/export-csv")
@role_required("student")
def export_csv_stub():
    return jsonify({"task_id": "demo-123", "message": "Celery wiring comes in Lesson 8"}), 202
```

Status **202 Accepted** is the correct HTTP code for "request received, processing will happen later" — remember this for the viva.

### Step 6.6: Run and Test the Full Stack

```bash
python app.py
```

1. Register a new student → log in → see the dashboard
2. Refresh the page → you should stay logged in (localStorage works)
3. Search drives, apply to one
4. Apply again → see the red "already applied" alert from the backend
5. Log out → log in as admin (approve the drive first if needed via Postman)

### Checkpoint 6

- Login + both registrations work in the browser
- Session survives refresh
- Student can search, apply, see the duplicate error
- Application status shows with a colored badge

### Quick Quiz (reply with answers)

1. Why do we use Jinja2 for only the entry point, and Vue for everything else?
2. What does v-model do, and how is it different from `value` + `addEventListener`?
3. Why does the frontend not hard-code error messages like "wrong password"?
4. Why is 202 the right status code for the export endpoint, not 200?

Next lesson — Lesson 7: Company and Admin dashboards in Vue (approving with buttons, applicant tables with status dropdowns, search). Then Lesson 8 — the big one: Redis caching + Celery jobs (daily reminders, monthly report, real CSV export).

Reply with quiz answers or "done + ready"

## User:

done + ready

## Kimi:

## Lesson 7: Company & Admin Dashboards in Vue

Great. Today we complete the UI so all three roles can do their jobs from the browser. The patterns are the same as Lesson 6 — if you understood those, this is mostly practice.

### Step 7.1: Company Dashboard — index.html

Replace the company placeholder div with:

```html
<!-- COMPANY DASHBOARD -->
<div v-if="page == 'company'">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>{{ companyDashboard.company?.name || 'Company Dashboard' }}</h3>
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
    </div>

    <!-- create drive form -->
    <div class="card mb-4 shadow-sm">
        <div class="card-body">
            <h5>Create Placement Drive</h5>
            <div class="row g-3">
                <div class="col-md-6">
                    <input class="form-control" placeholder="Job Title *" v-model="newDrive.job_title" required>
                </div>
                <div class="col-md-6">
                    <label class="form-label small mb-0">Application Deadline *</label>
                    <input type="datetime-local" class="form-control" v-model="newDrive.application_deadline" required>
                </div>
                <div class="col-12">
                    <textarea class="form-control" rows="2" placeholder="Job description" v-model="newDrive.job_description"></textarea>
                </div>
                <div class="col-md-4">
                    <input class="form-control" placeholder="Eligible branch (blank = all)" v-model="newDrive.eligible_branch">
                </div>
                <div class="col-md-4">
                    <input type="number" step="0.01" min="0" max="10" class="form-control"
                           placeholder="Min CGPA" v-model="newDrive.min_cgpa">
                </div>
                <div class="col-md-4">
                    <input type="number" min="1" max="4" class="form-control"
                           placeholder="Eligible year (blank = all)" v-model="newDrive.eligible_year">
                </div>
            </div>
            <button class="btn btn-success mt-3" @click="createDrive">Create Drive</button>
            <small class="text-muted d-block">Drives are invisible to students until the admin approves them.</small>
        </div>
    </div>

    <!-- my drives -->
    <div class="card shadow-sm">
        <div class="card-body">
            <h5>My Drives</h5>
            <table class="table table-hover">
                <thead><tr><th>Job Title</th><th>Status</th><th>Deadline</th><th>Applicants</th><th></th></tr></thead>
                <tbody>
                    <tr v-for="d in companyDashboard.drives" :key="d.id">
                        <td>{{ d.job_title }}</td>
                        <td><span class="badge" :class="driveBadge(d.status)">{{ d.status }}</span></td>
                        <td>{{ d.deadline.slice(0,10) }}</td>
                        <td>{{ d.applicant_count }}</td>
                        <td><button class="btn btn-sm btn-outline-primary" @click="viewApplicants(d.id)">View</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- applicants modal -->
    <div v-if="selectedDrive" class="card mt-4 shadow-sm border-primary">
        <div class="card-body">
            <div class="d-flex justify-content-between">
                <h5>Applicants — {{ selectedDriveTitle }}</h5>
                <button class="btn-close" @click="selectedDrive = null"></button>
            </div>
            <table class="table table-striped">
                <thead><tr><th>Name</th><th>Branch</th><th>CGPA</th><th>Year</th><th>Status</th><th></th></tr></thead>
                <tbody>
                    <tr v-for="a in applicants" :key="a.application_id">
                        <td>{{ a.student.name }}</td>
                        <td>{{ a.student.branch }}</td>
                        <td>{{ a.student.cgpa }}</td>
                        <td>{{ a.student.year }}</td>
                        <td><span class="badge" :class="statusBadge(a.status)">{{ a.status }}</span></td>
                        <td>
                            <select class="form-select form-select-sm" style="width: 130px;"
                                    v-model="a.status" @change="updateStatus(a.application_id, a.status)">
                                <option value="applied">Applied</option>
                                <option value="shortlisted">Shortlisted</option>
                                <option value="selected">Selected</option>
                                <option value="rejected">Rejected</option>
                            </select>
                        </td>
                    </tr>
                    <tr v-if="applicants.length === 0"><td colspan="6" class="text-muted">No applicants yet.</td></tr>
                </tbody>
            </table>
        </div>
    </div>
    <div v-if="message" class="alert mt-3" :class="messageType">{{ message }}</div>
</div>
```

**Why a `<select>` for status instead of separate buttons?**
Four buttons per row = cluttered and error-prone. A dropdown bound with `v-model="a.status"` lets us detect **change** (`@change`) and send only what changed. Also notice `v-model` on `a.status` — when the backend confirms, the badge updates instantly because Vue is reactive. No page reload, ever.

### Step 7.2: Admin Dashboard — index.html

Replace the admin placeholder div with:

```html
<!-- ========== ADMIN DASHBOARD ========== -->
<div v-if="page === 'admin'">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3>Admin Dashboard</h3>
        <button class="btn btn-outline-danger btn-sm" @click="logout">Logout</button>
    </div>

    <!-- stat cards -->
    <div class="row g-3 mb-4">
        <div class="col-6 col-md-3" v-for="stat in adminStats" :key="stat.label">
            <div class="card text-center shadow-sm">
                <div class="card-body py-3">
                    <h3 class="mb-0">{{ stat.value }}</h3>
                    <small class="text-muted">{{ stat.label }}</small>
                </div>
            </div>
        </div>
    </div>

    <!-- tabs for companies / drives / students -->
    <ul class="nav nav-tabs mb-3">
        <li class="nav-item"><a class="nav-link" :class="{active: adminTab==='companies'}" href="#" @click.prevent="adminTab='companies'; loadAdminCompanies()">Companies</a></li>
        <li class="nav-item"><a class="nav-link" :class="{active: adminTab==='drives'}" href="#" @click.prevent="adminTab='drives'; loadAdminDrives()">Drives</a></li>
        <li class="nav-item"><a class="nav-link" :class="{active: adminTab==='students'}" href="#" @click.prevent="adminTab='students'; loadAdminStudents()">Students</a></li>
    </ul>

    <!-- companies -->
    <div v-if="adminTab==='companies'">
        <input class="form-control mb-3" placeholder="Search companies..." v-model="companySearch" @input="loadAdminCompanies">
        <table class="table table-striped">
            <thead><tr><th>Name</th><th>Website</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
                <tr v-for="c in adminCompanies" :key="c.id">
                    <td>{{ c.name }}</td><td>{{ c.website }}</td>
                    <td><span class="badge" :class="companyBadge(c)">{{ c.is_blacklisted ? 'blacklisted' : c.approval_status }}</span></td>
                    <td>
                        <button v-if="c.approval_status==='pending'" class="btn btn-sm btn-success" @click="adminAction('/api/admin/companies/'+c.id+'/approve')">Approve</button>
                        <button v-if="c.approval_status==='pending'" class="btn btn-sm btn-outline-danger" @click="adminAction('/api/admin/companies/'+c.id+'/reject')">Reject</button>
                        <button class="btn btn-sm" :class="c.is_blacklisted ? 'btn-outline-dark' : 'btn-dark'"
                                @click="adminAction('/api/admin/companies/'+c.id+'/blacklist')">
                            {{ c.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
                        </button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- drives -->
    <div v-if="adminTab==='drives'">
        <input class="form-control mb-3" placeholder="Search drives..." v-model="driveAdminSearch" @input="loadAdminDrives">
        <table class="table table-striped">
            <thead><tr><th>Job Title</th><th>Company</th><th>Deadline</th><th>Status</th><th>Actions</th></tr></thead>
            <tbody>
                <tr v-for="d in adminDrives" :key="d.id">
                    <td>{{ d.job_title }}</td><td>{{ d.company }}</td><td>{{ d.deadline.slice(0,10) }}</td>
                    <td><span class="badge" :class="driveBadge(d.status)">{{ d.status }}</span></td>
                    <td>
                        <button v-if="d.status==='pending'" class="btn btn-sm btn-success" @click="adminAction('/api/admin/drives/'+d.id+'/approve')">Approve</button>
                        <button v-if="d.status==='pending'" class="btn btn-sm btn-outline-danger" @click="adminAction('/api/admin/drives/'+d.id+'/reject')">Reject</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- students -->
    <div v-if="adminTab==='students'">
        <input class="form-control mb-3" placeholder="Search students..." v-model="studentSearch" @input="loadAdminStudents">
        <table class="table table-striped">
            <thead><tr><th>Name</th><th>Branch</th><th>CGPA</th><th>Year</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
                <tr v-for="s in adminStudents" :key="s.id">
                    <td>{{ s.name }}</td><td>{{ s.branch }}</td><td>{{ s.cgpa }}</td><td>{{ s.year }}</td>
                    <td><span class="badge" :class="s.is_active ? 'bg-success' : 'bg-danger'">{{ s.is_active ? 'active' : 'deactivated' }}</span></td>
                    <td><button class="btn btn-sm btn-outline-warning" @click="adminAction('/api/admin/students/'+s.user_id+'/deactivate')">
                        {{ s.is_active ? 'Deactivate' : 'Reactivate' }}
                    </button></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-if="message" class="alert mt-3" :class="messageType">{{ message }}</div>
</div>
```

### Step 7.3: Add the New State & Methods to app.js

Add to the `data()` return object:

```javascript
companyDashboard: { company: {}, drives: [] },
newDrive: { job_title: '', application_deadline: '', job_description: '', eligible_branch: '', min_cgpa: '', eligible_year: '' },
selectedDrive: null,
selectedDriveTitle: '',
applicants: [],
adminTab: 'companies',
adminStats: [],
adminCompanies: [],
companySearch: '',
adminDrives: [],
driveAdminSearch: '',
adminStudents: [],
studentSearch: '',
```

Add these methods:

```javascript
// --- COMPANY ---
async loadCompanyDashboard() {
    try {
        this.companyDashboard = await this.api('/api/company/dashboard');
    } catch (e) { this.notify(e.message, true); }
},
async createDrive() {
    try {
        await this.api('/api/company/drives', {
            method: 'POST', body: JSON.stringify(this.newDrive),
        });
        this.notify('Drive created - awaiting admin approval.');
        this.newDrive = { job_title: '', application_deadline: '', job_description: '', eligible_branch: '', min_cgpa: '', eligible_year: '' };
        this.loadCompanyDashboard();
    } catch (e) { this.notify(e.message, true); }
},
async viewApplicants(driveId) {
    try {
        this.applicants = await this.api(`/api/company/drives/${driveId}/applications`);
        this.selectedDrive = driveId;
        this.selectedDriveTitle = this.companyDashboard.drives.find(d => d.id == driveId)?.job_title || '';
    } catch (e) { this.notify(e.message, true); }
},
async updateStatus(appId, status) {
    try {
        await this.api(`/api/company/applications/${appId}/status`, {
            method: 'POST', body: JSON.stringify({ status }),
        });
        this.notify(`Application marked ${status}`);
    } catch (e) { this.notify(e.message, true); }
},

// --- ADMIN ---
async loadAdminStats() {
    try {
        const d = await this.api('/api/admin/dashboard');
        this.adminStats = [
            { label: 'Students', value: d.total_students },
            { label: 'Companies', value: d.total_companies },
            { label: 'Drives', value: d.total_drives },
            { label: 'Pending Companies', value: d.pending_companies },
            { label: 'Pending Drives', value: d.pending_drives },
        ];
    } catch (e) { this.notify(e.message, true); }
},
async loadAdminCompanies() {
    const url = '/api/admin/companies' + (this.companySearch ? '?q=' + encodeURIComponent(this.companySearch) : '');
    this.adminCompanies = await this.api(url);
},
async loadAdminDrives() {
    const url = '/api/admin/drives' + (this.driveAdminSearch ? '?q=' + encodeURIComponent(this.driveAdminSearch) : '');
    this.adminDrives = await this.api(url);
},
async loadAdminStudents() {
    const url = '/api/admin/students' + (this.studentSearch ? '?q=' + encodeURIComponent(this.studentSearch) : '');
    this.adminStudents = await this.api(url);
},

// One reusable helper for every admin action button - DRY principle!
async adminAction(url) {
    try {
        const data = await this.api(url, { method: 'POST' });
        this.notify(data.message);
        this.loadAdminStats();
        if (this.adminTab === 'companies') this.loadAdminCompanies();
        if (this.adminTab === 'drives') this.loadAdminDrives();
        if (this.adminTab === 'students') this.loadAdminStudents();
    } catch (e) { this.notify(e.message, true); }
},

// badge helpers
driveBadge(status) {
    return { pending: 'bg-warning text-dark', approved: 'bg-success', rejected: 'bg-danger', closed: 'bg-secondary' }[status] || 'bg-secondary';
},
companyBadge(c) {
    if (c.is_blacklisted) return 'bg-dark';
    return { pending: 'bg-warning text-dark', approved: 'bg-success', rejected: 'bg-danger' }[c.approval_status] || 'bg-secondary';
},
```

Update `doLogin` so dashboards load for all roles:

```javascript
if (data.role === 'student') { this.page = 'student'; this.loadDrives(); this.loadApplications(); }
else if (data.role === 'company') { this.page = 'company'; this.loadCompanyDashboard(); }
else { this.page = 'admin'; this.loadAdminStats(); this.loadAdminCompanies(); }
```

And update `mounted()` similarly:

```javascript
if (token && role) {
    this.page = role;
    if (role === 'student') { this.loadDrives(); this.loadApplications(); }
    if (role === 'company') this.loadCompanyDashboard();
    if (role === 'admin') { this.loadAdminStats(); this.loadAdminCompanies(); }
}
```

### Step 7.4: Notice the Design Principle — DRY

Look at `adminAction(url)`. Six different buttons all call it with different URLs.

**Don't Repeat Yourself** — one function, many callers. When the examiner asks "how did you structure your frontend?", say: "a generic `api()` helper for HTTP, and a generic `adminAction()` for all state-changing admin operations, so each button is one line."

### Step 7.5: Full Three-Role UI Test

1. **Admin:** log in → see stat cards → approve company & drive → blacklist/unblacklist → search a student
2. **Company:** log in → create drive → see it as pending → (admin approves) → refresh → see it approved → view applicants → change status in dropdown → verify student sees it
3. **Student:** log in → apply → watch status badge change live when company updates it

Test on a narrow browser window too — Bootstrap's grid (`col-6 col-md-3`) makes it responsive for free. Mention that in the demo.

### Checkpoint 7

- Company can create a drive, view applicants, change statuses
- Admin sees stat cards, can approve/reject/blacklist, search all three entities
- Status changes made by company appear on student's screen after refresh

### Quick Quiz (reply with answers)

1. Why is a `<select>` with `@change` better than four separate buttons per applicant?
2. What does the `adminAction()` helper demonstrate? (Name the principle.)
3. Why does the company dashboard need a refresh after admin approves a drive, rather than updating instantly? What technology would fix that? (Hint: something that pushes updates from server → client.)
4. How does `v-model` on the status `<select>` keep the badge in sync?

Next lesson — Lesson 8 (the big one): Redis caching + Celery. We'll wire up the real CSV export with email/webhook notification, daily deadline reminders, and the monthly admin report. This is the section where most students lose marks — we'll do it carefully.

Reply with quiz answers or "done + ready"

## User:

done + ready

## Kimi:

## Lesson 8: Redis Caching + Celery Background Jobs (The Big One)

This is where most projects lose marks. We'll go slowly. First concepts, then code, then testing.

### Step 8.1: Concepts First — Understand Before You Code

#### What is Celery, and why do we need it?

Some work must not happen inside an HTTP request:

| Job | Why it can't run in the request |
|---|---|
| CSV export | Takes seconds-minutes; user shouldn't stare at a spinning page |
| Daily reminders | Must run at a scheduled time, with no user triggering it |
| Monthly report | Runs on the 1st of the month, even if nobody is online |

Celery solves this. The pattern:

```
Flask (web request)
  → "hey Celery, do task X" → puts a message in Redis (the BROKER)
  → returns 202 immediately

Celery Worker (a SEPARATE process) watches Redis, picks up the message, executes the task
```

Three pieces, and you must start each: **Redis** (broker), **Celery worker** (does the work), **Celery beat** (the scheduler that triggers periodic tasks).

Docs: https://docs.celeryq.dev/en/stable/getting-started/introduction.html - read the "What is Celery?" + "Brokers" sections.

#### What is Redis caching — and where do we use it?

The admin dashboard counts (`Student.query.count()`, etc.) hit SQLite on every page load. Dashboards change rarely but are viewed constantly — the classic caching case.

**Pattern: cache-aside**

```
request → check Redis first
  hit?  → return cached value (fast!)
  miss? → query SQLite, store result in Redis WITH EXPIRY, return
```

Expiry is mandatory (project doc requires it). We'll use 60 seconds for dashboards — stale data disappears automatically, and we manually delete the key whenever data changes (e.g., after approvals) so updates appear quickly.

### 8.2: Create the Celery App — backend/jobs/celery_app.py

```python
# backend/jobs/celery_app.py
from celery import Celery
from celery.schedules import crontab

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config["CELERY_BROKER_URL"],
        backend=app.config["CELERY_RESULT_BACKEND"],
    )
    celery.conf.update(app.config)
    celery.conf.timezone = "UTC"

    # --- Periodic schedule ---
    celery.conf.beat_schedule = {
        "daily-deadline-reminders": {
            "task": "jobs.tasks.send_deadline_reminders",
            "schedule": crontab(hour=9, minute=0),  # every day 09:00 UTC
        },
        "monthly-admin-report": {
            "task": "jobs.tasks.send_monthly_report",
            "schedule": crontab(day_of_month=1, hour=0, minute=5),  # 1st of month
        },
    }
    return celery
```

**Why a separate `make_celery` factory?** The Celery worker and the Flask app need to share configuration, but they run in different processes. The factory builds the Celery instance from the Flask config so there's one source of truth.

### Step 8.3: The Tasks — backend/jobs/tasks.py

Create the shared email-sending utility first. For a local demo, we'll use Gmail SMTP via an app password — the simplest reliable option. Create `backend/jobs/mailer.py`:

```python
# backend/jobs/mailer.py
import smtplib
from email.mime.text import MIMEText

# For demo only - real apps use env vars!
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "your.email@gmail.com"          # ← change this
SMTP_PASSWORD = "your_app_password"         # ← Gmail app password, NOT login pw
ADMIN_EMAIL = "admin@institute.edu"

def send_email(to, subject, html):
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = to
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)
```

Docs: Gmail app passwords → https://support.google.com/accounts/answer/185833 (refer here when setting up — you need 2FA enabled).

Now the tasks:

```python
# backend/jobs/tasks.py
import csv, os
from datetime import datetime, timedelta
from celery import shared_task
from models import db, Student, PlacementDrive, Application, User
from jobs.mailer import send_email, ADMIN_EMAIL

EXPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# --- (c) User-triggered async job: export applications as CSV ---
@shared_task
def export_applications_csv(student_user_id):
    """
    Runs in the worker. Queries the DB, writes a CSV,
    emails the student when done.
    """
    student = Student.query.filter_by(user_id=student_user_id).first()
    if not student:
        return "no such student"

    apps = Application.query.filter_by(student_id=student.id).all()
    filename = f"applications_student_{student.id}_{int(datetime.utcnow().timestamp())}.csv"
    path = os.path.join(EXPORT_DIR, filename)

    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Application ID", "Student ID", "Company Name", "Drive Title", "Status", "Applied At"])
        for a in apps:
            writer.writerow([
                a.id, student.id,
                a.drive.company.name if a.drive.company else "",
                a.drive.job_title, a.status,
                a.applied_at.strftime("%Y-%m-%d %H:%M"),
            ])

    # Notify: email the student
    send_email(
        to=student.user.email,
        subject="Your placement applications export is ready",
        html=f"<p>Hi {student.name},</p><p>Your CSV export with {len(apps)} "
             f"application(s) is ready. File: <b>{filename}</b> "
             f"(in the server <code>exports</code> folder).</p>"
    )
    return filename

# --- (a) Scheduled job: daily deadline reminders ---
@shared_task
def send_deadline_reminders():
    """
    Every morning: find drives whose deadline is within 48 hours,
    email all eligible students who haven't applied yet.
    """
    soon = datetime.utcnow() + timedelta(hours=48)
    drives = PlacementDrive.query.filter(
        PlacementDrive.status == "approved",
        PlacementDrive.application_deadline > datetime.utcnow(),
        PlacementDrive.application_deadline <= soon,
    ).all()

    sent = 0
    for drive in drives:
        for student in Student.query.all():
            # Skip if not eligible or already applied
            if drive.eligible_branch and student.branch != drive.eligible_branch:
                continue
            if student.cgpa is not None and student.cgpa < drive.min_cgpa:
                continue
            already = Application.query.filter_by(
                student_id=student.id, drive_id=drive.id).first()
            if already:
                continue
            send_email(
                to=student.user.email,
                subject=f"Deadline soon: {drive.job_title} at {drive.company.name}",
                html=f"<p>Hi {student.name},</p><p>The application deadline for "
                     f"<b>{drive.job_title}</b> at <b>{drive.company.name}</b> is "
                     f"<b>{drive.application_deadline.strftime('%Y-%m-%d')}</b>. Apply soon!</p>",
            )
            sent += 1
    return f"reminders sent: {sent}"

# --- (b) Scheduled job: monthly activity report ---
@shared_task
def send_monthly_report():
    """First day of month: build an HTML report for the admin and email it."""
    drives = PlacementDrive.query.filter(
        PlacementDrive.status.in_(["approved", "closed"])).all()
    applications = Application.query.all()

    rows = "".join(
        f"<tr><td>{d.job_title}</td><td>{d.company.name}</td>"
        f"<td>{d.status}</td><td>{len(d.applications)}</td></tr>"
        for d in drives
    )
    selected = sum(1 for a in applications if a.status == "selected")

    html = f"""
    <h2>Monthly Placement Activity Report - {datetime.utcnow().strftime('%B %Y')}</h2>
    <p><b>Total drives:</b> {len(drives)} &nbsp; <b>Total applications:</b> {len(applications)} &nbsp; <b>Students selected:</b> {selected}</p>
    <table border="1" cellpadding="6" cellspacing="0">
      <tr><th>Drive</th><th>Company</th><th>Status</th><th>Applicants</th></tr>
      {rows}
    </table>
    """
    send_email(to=ADMIN_EMAIL, subject="Monthly Placement Report", html=html)
    return "report sent"
```

**Why `@shared_task`?** It lets Celery discover tasks without the worker importing the Flask app directly. Clean separation.

**Notice the export task takes `student_user_id`, not `student_id`** — because the JWT identity is the user id, and the worker shouldn't trust whatever the browser sends. We look up the student from the user id.

### Step 8.4: Wire Everything Into app.py

Update `app.py`:

```python
# --- new imports ---
from jobs.celery_app import make_celery
from jobs import tasks  # noqa: F401 (registers tasks with Celery)
import redis

# after app/db setup:
celery = make_celery(app)
cache = redis.Redis.from_url(app.config["REDIS_URL"])
```

And replace the CSV stub in `routes/student.py`:

```python
# replace export_csv_stub with:
from jobs.tasks import export_applications_csv

@student_bp.post("/export-csv")
@role_required("student")
def export_csv():
    task = export_applications_csv.delay(current_user_id())  # async! returns instantly
    return jsonify({"task_id": task.id}), 202
```

**`.delay()` is the magic line.** It doesn't run the function — it queues a message in Redis and returns a task object immediately. The web request finishes in milliseconds. This is the difference between a blocking endpoint and an async one — expect this question in the viva.

### 8.5: Add Caching to the Admin Dashboard

Update `routes/admin.py` — the dashboard endpoint:

```python
import redis, json
from flask import current_app

@admin_bp.get("/dashboard")
@role_required("admin")
def dashboard():
    cache = redis.Redis.from_url(current_app.config["REDIS_URL"])
    CKEY = "admin:dashboard"

    cached = cache.get(CKEY)
    if cached:                     # cache HIT
        return jsonify(json.loads(cached))

    data = {                       # cache MISS → query SQLite
        "total_students": Student.query.count(),
        "total_companies": Company.query.count(),
        "total_drives": PlacementDrive.query.count(),
        "pending_companies": Company.query.filter_by(approval_status="pending").count(),
        "pending_drives": PlacementDrive.query.filter_by(status="pending").count(),
    }

    cache.setex(CKEY, 60, json.dumps(data))  # store for 60 seconds expiry
    return jsonify(data)
```

And invalidate the cache whenever counts change — add this helper at the top of `admin.py`:

```python
def invalidate_dashboard_cache():
    redis.Redis.from_url(current_app.config["REDIS_URL"]).delete("admin:dashboard")
```

Call `invalidate_dashboard_cache()` inside every mutating admin endpoint (approve/reject/blacklist/deactivate) right after `db.session.commit()`.

**Why both TTL and manual invalidation?** TTL (60s) is a safety net so data never stays stale forever; manual deletion makes updates visible instantly. This two-layer strategy is exactly what a good answer to "how did you handle cache consistency?" sounds like.

### 8.6: Run the Full Stack — Three Terminals

```bash
# Terminal 1 - Redis (should already be running from Lesson 1)
redis-server

# Terminal 2 - Celery worker
cd backend
celery -A app.celery worker --loglevel=info -P solo
# (-P solo avoids prefork issues on Windows)

# Terminal 3 - Celery beat (scheduler)
celery -A app.celery beat --loglevel=info

# Terminal 4 - Flask
python app.py
```

Docs: running the worker → https://docs.celeryq.dev/en/stable/userguide/workers.html

**Test the CSV export:**
1. Log in as a student in the browser → click "Export as CSV"
2. Instantly see "Export started - task ..." (the 202)
3. Check Terminal 2 — worker logs show the task completing
4. Check the `backend/exports/` folder — CSV file appears
5. Check your email — notification arrives

**Test a scheduled job without waiting:** in a Python shell:

```python
from jobs.tasks import send_monthly_report
send_monthly_report.delay()  # manually trigger via the same queue
```

Watch the worker pick it up. (For your demo, manual triggering is fine to show; the schedule itself is configured via beat_schedule.)

**Test caching:**
1. `GET /api/admin/dashboard` — first call is slow-ish
2. Immediately again — instant
3. In Terminal 1 run `redis-cli - GET admin:dashboard` — you'll see the JSON
4. After 60s it vanishes (TTL admin:dashboard counts down) → expiry proven

### Checkpoint 8

- CSV export: button → 202 → worker runs → file appears → email arrives
- Monthly report task can be triggered manually and emails the admin
- Dashboard second call is served from Redis (verify with redis-cli)
- Cache expires after 60s AND invalidates instantly after an approval
- You can start all four processes from memory

### Quick Quiz (reply with answers)

1. What does `.delay()` actually do, and why does the HTTP request return in milliseconds?
2. What are the three pieces of Celery infrastructure you must start, and what does each do?
3. Why do we use both TTL expiry and manual invalidation? What failure does each protect against?
4. Why does the export task take `student_user_id` and look up the student, instead of accepting `student_id` directly from the browser?

Next lesson — Lesson 9: Polish & submission prep: resume upload, report writing (ER diagram, API endpoints table, AI declaration), video script, and viva prep with the 10 most likely questions.

Reply with quiz answers or "done + ready"

## User:

done + ready

## Kimi:

## Lesson 9: Polish, Report, Video & Viva Preparation

Final stretch. Your app works — now we make it submission-grade. This lesson is about the deliverables that get marks: resume upload, the 5-page report, the video, and surviving the viva.

### Step 9.1: Resume Upload (a Required Feature We Deferred)

Students must "edit their profile and upload resume." We need file handling — a new topic, so listen carefully.

**Backend — add to `routes/student.py`:**

```python
import os
from flask import current_app
from werkzeug.utils import secure_filename

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
ALLOWED = {"pdf", "doc", "docx"}

@student_bp.post("/resume")
@role_required("student")
def upload_resume():
    student = get_my_student()

    if "resume" not in request.files:
        return jsonify({"error": "no file part named 'resume'"}), 400
    file = request.files["resume"]

    if file.filename == "":
        return jsonify({"error": "no file selected"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED:
        return jsonify({"error": "only pdf/doc/docx allowed"}), 400

    # secure_filename strips dangerous paths like ../etc/passwd
    filename = secure_filename(f"student_{student.id}_{file.filename}")
    file.save(os.path.join(UPLOAD_DIR, filename))

    student.resume_filename = filename
    db.session.commit()
    return jsonify({"message": "resume uploaded", "filename": filename}), 200
```

Also add a GET route so companies can view it later:

```python
@student_bp.get("/resume/<int:student_id>")
@role_required("company", "student", "admin")
def get_resume(student_id):
    student = Student.query.get_or_404(student_id)
    # students may only fetch their OWN resume
    if current_user_id() != student.user_id:
        from flask_jwt_extended import get_jwt
        if get_jwt().get("role") not in ("admin", "company"):
            return jsonify({"error": "forbidden"}), 403
    if not student.resume_filename:
        return jsonify({"error": "no resume uploaded"}), 404
    from flask import send_from_directory
    return send_from_directory(UPLOAD_DIR, student.resume_filename)
```

#### Why these security details (viva gold)

1. `secure_filename` — without it, a malicious filename like `../../.bashrc` could overwrite system files. Never trust uploaded filenames.
2. **Extension allow-list** — blocks `.exe`, `.sh`, `.php` uploads.
3. `send_from_directory` (not `send_file` with a raw path) — prevents path traversal attacks where `../../` in a URL escapes the uploads folder.
4. **Role check on viewing** — a student can only download their own resume; companies/admins can view any.

Docs: file uploads → https://flask.palletsprojects.com/patterns/fileuploads/

**Frontend — add to the student dashboard `index.html`:**

```html
<div class="card mb-4 shadow-sm">
    <div class="card-body">
        <h5>My Resume</h5>
        <input type="file" class="form-control mb-2" accept=".pdf,.doc,.docx" @change="uploadResume" ref="resumeInput">
        <small v-if="resumeName" class="text-muted">Current: {{ resumeName }}</small>
    </div>
</div>
```

And in `app.js`:

```javascript
async uploadResume(event) {
    const file = event.target.files[0];
    if (!file) return;
    const formData = new FormData();
    formData.append("resume", file);
    try {
        const token = localStorage.getItem("token");
        const res = await fetch("/api/student/resume", {
            method: "POST",
            headers: { "Authorization": "Bearer " + token },  // NO Content-Type!
            body: formData,
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);
        this.resumeName = data.filename;
        this.notify("Resume uploaded ✓");
    } catch (e) { this.notify(e.message, true); }
},
```

**Key gotcha:** when sending FormData, do **not** set `Content-Type: application/json` — the browser must set the `multipart/form-data` boundary itself. This trips up many students; now it won't trip you. Add `resumeName: ''` to `data()` and set it after `loadApplications()` — or simply leave it updated on upload.

### Step 9.2: The Project Report (≤5 pages)

Your report must contain, per the doc: student details, project details + approach, AI/LLM declaration, frameworks used, ER diagram, API endpoints, and video link. Here's your structure, page by page:

**Page 1 — Cover:** name, roll no, course, project title, date.

**Page 2 — Introduction & Approach (½ page) + Frameworks table (½ page):**
- Problem statement in 2–3 lines
- Approach: "Three-tier architecture — Vue.js frontend consuming a Flask REST API, with SQLAlchemy models on SQLite, Redis for caching, and Celery workers for asynchronous jobs."
- Frameworks table: Flask, Flask-SQLAlchemy, Flask-JWT-Extended, Vue 3 (CDN), Bootstrap 5, SQLite, Redis, Celery — with a one-line "why" for each (you know these by heart now!)

**Page 3 — ER Diagram:** redraw the diagram from Lesson 2.1 neatly. Show PKs, FKs, and the 1:1 / 1:N / M:N relationships. Add a 3-line explanation of the junction table (Application).

**Page 4 — API Endpoints table (this is easy — you built all of them):**

| Endpoint | Method | Auth | Description |
|---|---|---|---|
| /api/register/student | POST | — | Student self-registration |
| /api/register/company | POST | — | Company registration (pending approval) |
| /api/login | POST | — | Login, returns JWT + role |
| /api/admin/dashboard | GET | admin | Dashboard counts (cached) |
| /api/admin/companies | GET | admin | List/search companies |
| /api/admin/companies/:id/approve | POST | admin | Approve company |
| /api/admin/companies/:id/blacklist | POST | admin | Toggle blacklist |
| /api/admin/drives/:id/approve | POST | admin | Approve drive |
| /api/admin/students/:id/deactivate | POST | admin | Toggle student active |
| /api/company/dashboard | GET | company | Company drives + applicant counts |
| /api/company/drives | POST | company | Create drive |
| /api/company/drives/:id/applications | GET | company | View applicants (ownership checked) |
| /api/company/applications/:id/status | POST | company | Shortlist/select/reject |
| /api/student/drives | GET | student | Browse approved, open drives |
| /api/student/drives/:id/apply | POST | student | Apply (eligibility + duplicate checks) |
| /api/student/applications | GET | student | My application history |
| /api/student/export-csv | POST | student | Queue CSV export (Celery) |
| /api/student/resume | POST | student | Upload resume |
| /api/student/resume/:id | GET | any | Download resume |

**Page 5 — AI/LLM Declaration + Video Link:** state clearly which AI tools you used and how (e.g., "used Kimi to help structure the Flask backend and review SQLAlchemy relationship syntax; all code was typed, tested, and understood by me"). Add your demo video link. This declaration is required by the doc — don't skip it.

### 9.3: The Demo Video (5-10 min)

Follow the doc's suggested script, but rehearse this exact flow — it tells a story:

1. **Intro (30s):** who you are, what PPA is, one line on the stack.
2. **Approach (30s):** show the folder structure + ER diagram slide.
3. **Core demo (4-6 min):** live in the browser —
   - Register student + company (show validation errors on purpose: duplicate email, weak input)
   - Login as company → blocked ("not approved") - this is a feature, show it proudly
   - Admin approves company → company logs in
   - Company creates drive → student can't see it → admin approves drive → student sees it
   - Show eligibility rejection, fix CGPA, apply, apply again → 409 duplicate
   - Company shortlists → student sees status update
   - Click CSV export → show 202 → cut to terminal → worker running → file + email
   - redis-cli showing cached dashboard + TTL counting down
4. **Extras (30-60s):** responsiveness (resize browser), resume upload.
5. **Close (15s):** what you'd add next (email via proper service, charts with ChartJS - optional features from the doc).

Record with OBS (free). Keep your face cam on - the doc says it's recommended. Speak to the story, not feature-by-feature.

### Step 9.4: Viva Prep - The 10 Questions You WILL Get

Rehearse one-paragraph answers out loud:

1. **"Why JWT over sessions?"** → Stateless, scales, API-first; token carries role claim signed server-side.
2. **"How does role-based access control work?"** → Role embedded in JWT at login; `role_required` decorator verifies signature + role on every request; 403 if wrong role, 401 if no token.
3. **"How did you prevent duplicate applications?"** → Two layers: app-level check + DB UniqueConstraint; race condition caught via IntegrityError.
4. **"What is a race condition?"** → Two simultaneous requests both pass the Python check; DB constraint is the final arbiter.
5. **"Why Redis + Celery?"** → Web requests must be fast; slow/scheduled work offloaded. Redis = broker + cache.
6. **"Cache invalidation strategy?"** → TTL (60s safety net) + manual deletion on mutations (instant consistency). Cache-aside pattern.
7. **"What is IDOR?"** → Example: company requesting another company's drive URL; prevented by ownership checks in every route.
8. **"Why SQLite and not MySQL?"** → Project constraint; zero-config, file-based, ACID-compliant, fine for local demo scale.
9. **"What happens if Redis is down?"** → (Honest answer!) Celery jobs fail/queue errors; for production add retries (`--max-retries`) and a circuit breaker; caching code should degrade gracefully — mention you'd wrap cache calls in try/except.
10. **"Explain the request lifecycle of applying to a drive."** → Walk through: Vue → POST with token → JWT verified → role checked → student fetched → 4 eligibility checks → duplicate check → insert → commit → 201 → Vue updates list.

### Step 9.5: Final Submission Checklist

- Delete `placement.db` and `uploads/`+`exports/` contents, re-run `python app.py` once — proves DB + admin are created programmatically from scratch
- Zip the whole project folder (excluding `venv/`— the portal instructions say so; graders recreate it via your requirements.txt). Create one: `pip freeze > requirements.txt`
- Record video → upload to Drive → link sharing ON (anyone with link)
- Report PDF ≤ 5 pages with all required sections
- Test the zip on a different folder/machine: fresh venv → `pip install -r requirements.txt` → run everything. This catches the #1 submission failure: "it worked on my machine."

### Checkpoint 9 (Final)

- Resume upload works with validation
- Report drafted with all 6 required sections
- Video recorded following the story flow
- Fresh-machine test of the zip passed

### Final Quiz

1. Why must you never set Content-Type manually when uploading with FormData?
2. What is path traversal, and which two functions prevent it in our upload code?
3. Say your answer to question 6 above out loud in under 30 seconds. Did you mention both TTL and manual invalidation?
4. What's the single most common submission failure, and which step above prevents it?

Congratulations — you've built the complete project. You now have: programmatic DB + admin, JWT auth with RBAC, full three-role business logic, security guards (IDOR, race conditions, path traversal), async jobs with Celery/Redis, caching with expiry, and all the submission artifacts.

If you want, we can do a mock viva next — I'll play the examiner and grill you on any weak spots. Or ask about any lesson you want to revisit.

## User:

yes lets do the mock viva

## Kimi:

## Mock Viva — Begin

*Puts on examiner glasses.*

Sit up straight. In the real viva, I'll ask questions, you'll answer, and I may interrupt you or go deeper based on what you say. I'll grade you honestly — **harsh but fair**, like a real examiner. This is practice; being wrong here is free.

**Rules of engagement:**
- Answer in your own words, like you'd speak out loud (short spoken-style answers, not essays)
- If you don't know, say "I don't know but I think..." — guessing intelligently is better than silence
- I'll rate each answer: **Strong / Weak / Wrong**, then tell you how to fix it

Let's begin.

### Question 1 (Warm-up, but don't be complacent)

"Walk me through what happens — step by step, from the moment a student clicks 'Apply' on a drive — all the way to the database. Don't skip the security parts."

*(I want: HTTP request → token verification → role check → ownership/lookup → eligibility checks → duplicate checks → insert → commit → response. And I'm listening for whether you mention 401 vs 403.)*

### Question 2

"Your application sends the JWT token from browser localStorage. What are the security risks of storing a token in localStorage? How would you mitigate them?"

*(This is a classic trap question. Most students say 'localStorage is safe.' If you say that, you fail. Think: XSS...)*

### Question 3

"Show me — or explain — how you would demonstrate that your caching is actually working during the demo. And follow-up: if the admin approves a company and immediately reloads the dashboard, will the count be correct? Why or why not?"

*(I'm testing whether you wired invalidation in. If you didn't, own it and say what you'd change — partial credit for honesty.)*

Take your time. Answer all three, then reply, and I'll grade each one and hit you with the next round.