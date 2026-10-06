# Placement Portal Application (PPA)

Flask + VueJS + SQLite + Redis + Celery campus placement management system.

## Prerequisites

- Python 3.10+
- Redis server (`redis-server` on your PATH, or run via Docker)
- SMTP account for outgoing mail (e.g. Gmail with an App Password) — optional but
  needed for the monthly report and export-ready emails
- A Google Chat incoming webhook URL — optional but needed for daily reminders

## 1. Install dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure environment

```bash
cp .env.example .env
# then edit .env and fill in REDIS_URL / MAIL_* / GCHAT_WEBHOOK_URL as needed
```

If you skip this step, the app still runs with sensible localhost defaults —
Redis on `localhost:6379`, and reminder/report emails will simply log a
warning and skip sending instead of crashing.

## 3. Create the database and bootstrap the admin (programmatic — no DB Browser)

```bash
python seed.py
```

This creates `backend/instance/placement_portal.sqlite3` with all tables via
SQLAlchemy model metadata, and inserts the single pre-existing Admin user
(email/password from `.env`, default `admin@placementportal.local` /
`Admin@123`). There is no admin registration route — this is the only way
an admin account is created.

## 4. Start Redis

```bash
redis-server
```

(Or with Docker: `docker run -p 6379:6379 redis`)

## 5. Start the Flask API

```bash
# from backend/
python app.py
# API is now at http://localhost:5000
```

## 6. Start the Celery worker (handles the async CSV export task)

In a new terminal:

```bash
cd backend
source venv/bin/activate
celery -A celery_worker.celery worker --loglevel=info
```

## 7. Start Celery Beat (handles the two scheduled jobs)

In another new terminal:

```bash
cd backend
source venv/bin/activate
celery -A celery_worker.celery beat --loglevel=info
```

- **Daily deadline reminders** fire once a day at `REMINDER_HOUR:REMINDER_MINUTE`
  (default 09:00 UTC) and post to `GCHAT_WEBHOOK_URL`.
- **Monthly activity report** fires at 06:00 UTC on the 1st of every month and
  emails every admin user an HTML summary.

To test either job immediately without waiting for the schedule, run it
directly from a Python shell:

```bash
cd backend
python -c "
from app import create_app
app = create_app()
with app.app_context():
    from tasks import send_daily_deadline_reminders, generate_monthly_report
    print(send_daily_deadline_reminders.run())
    print(generate_monthly_report.run())
"
```

## 8. (Optional) Combined worker + beat for local demos

For a single-terminal demo you can run worker and beat together:

```bash
celery -A celery_worker.celery worker --beat --loglevel=info
```

## Project structure

```
placement-portal/
├── backend/
│   ├── app.py              # Flask app factory + Celery Beat schedule
│   ├── config.py
│   ├── extensions.py       # db, jwt, cache, celery instances
│   ├── models.py           # User, Student, Company, Drive, Application
│   ├── seed.py              # programmatic DB creation + admin bootstrap
│   ├── tasks.py             # 3 Celery tasks (reminders, report, csv export)
│   ├── celery_worker.py
│   ├── utils/notifications.py   # Google Chat + SMTP helpers
│   ├── templates_email/monthly_report.html
│   ├── api/
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── company.py
│   │   ├── student.py
│   │   └── decorators.py    # role_required JWT decorator
│   └── requirements.txt
└── frontend/
    ├── templates/index.html # Jinja2 CDN entry point only
    └── static/js, static/css # VueJS app (built in a later stage)
```

## API overview (role-gated via JWT)

| Area | Base path |
|---|---|
| Auth | `/api/auth/*` — register/student, register/company, login, me |
| Admin | `/api/admin/*` — dashboard, companies, students, drives, applications |
| Company | `/api/company/*` — profile, dashboard, drives, applications |
| Student | `/api/student/*` — profile, resume, drives, applications, export |

See the code in `backend/api/` for full endpoint list and payloads.

## Optional feature: dummy offer letter generator

Once a company marks an application as `Selected`, they can download a
generated PDF offer letter from the applicants view (`GET
/api/company/applications/<id>/offer-letter`). The PDF is clearly marked as
a sample/demo document and is not a legally binding offer — this satisfies
the project's optional "dummy offer letter generator" requirement.
