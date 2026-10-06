"""
Celery tasks:
    - send_daily_deadline_reminders  (Celery Beat, daily) -> Google Chat webhook
    - generate_monthly_report        (Celery Beat, 1st of month) -> email to admin
    - export_applications_csv_task   (user-triggered, async) -> CSV file + email alert

All tasks run inside the Flask app context (see extensions.make_celery /
app.py's ContextTask) so they can use the SQLAlchemy models directly.
"""
import os
import csv
import logging
from datetime import datetime, timedelta

from flask import current_app, render_template_string

from extensions import celery, db
from models import User, Student, Company, Drive, Application
from utils.notifications import send_gchat_message, send_email

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# a) Daily deadline reminders -> Google Chat webhook
# ---------------------------------------------------------------------------
@celery.task(name="tasks.send_daily_deadline_reminders")
def send_daily_deadline_reminders(days_ahead=3):
    """
    Finds drives whose application deadline falls within the next
    `days_ahead` days and posts a reminder to the configured Google Chat
    webhook, listing affected drives and how many students have applied
    so far. Intended to run once a day via Celery Beat.
    """
    webhook_url = current_app.config.get("GCHAT_WEBHOOK_URL")

    now = datetime.utcnow()
    window_end = now + timedelta(days=days_ahead)

    upcoming_drives = (
        Drive.query.filter(
            Drive.status == "Approved",
            Drive.application_deadline >= now,
            Drive.application_deadline <= window_end,
        )
        .order_by(Drive.application_deadline.asc())
        .all()
    )

    if not upcoming_drives:
        logger.info("No drives with deadlines in the next %s days. No reminder sent.", days_ahead)
        return {"drives_notified": 0}

    lines = [f"*Placement Portal — Upcoming Deadlines (next {days_ahead} days)*"]
    for d in upcoming_drives:
        applied_count = Application.query.filter_by(drive_id=d.id).count()
        deadline_str = d.application_deadline.strftime("%d %b %Y, %H:%M UTC")
        company_name = d.company.name if d.company else "Unknown company"
        lines.append(
            f"- {company_name} — {d.job_title}: deadline {deadline_str} "
            f"({applied_count} application(s) so far)"
        )

    message = "\n".join(lines)
    sent = send_gchat_message(webhook_url, message)

    logger.info("Daily reminder sent=%s for %s drive(s).", sent, len(upcoming_drives))
    return {"drives_notified": len(upcoming_drives), "sent": sent}


# ---------------------------------------------------------------------------
# b) Monthly activity report -> email to admin
# ---------------------------------------------------------------------------
@celery.task(name="tasks.generate_monthly_report")
def generate_monthly_report():
    """
    Summarizes placement activity for the previous calendar month:
    drives conducted, students applied, students selected. Renders an HTML
    email and sends it to every admin user. Intended to run on the 1st of
    every month via Celery Beat.
    """
    today = datetime.utcnow()
    first_of_this_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day_prev_month = first_of_this_month - timedelta(seconds=1)
    first_of_prev_month = last_day_prev_month.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    period_label = first_of_prev_month.strftime("%B %Y")

    drives_in_period = Drive.query.filter(
        Drive.created_at >= first_of_prev_month,
        Drive.created_at <= last_day_prev_month,
    ).all()

    drive_rows = []
    total_applied = 0
    total_selected = 0
    for d in drives_in_period:
        applicant_count = Application.query.filter_by(drive_id=d.id).count()
        selected_count = Application.query.filter_by(drive_id=d.id, status="Selected").count()
        total_applied += applicant_count
        total_selected += selected_count
        drive_rows.append(
            {
                "company_name": d.company.name if d.company else "Unknown",
                "job_title": d.job_title,
                "applicant_count": applicant_count,
                "selected_count": selected_count,
            }
        )

    template_path = os.path.join(
        os.path.dirname(__file__), "templates_email", "monthly_report.html"
    )
    with open(template_path, "r", encoding="utf-8") as f:
        template_str = f.read()

    html_body = render_template_string(
        template_str,
        period_label=period_label,
        drives_conducted=len(drives_in_period),
        students_applied=total_applied,
        students_selected=total_selected,
        drives=drive_rows,
    )

    admins = User.query.filter_by(role="admin").all()
    results = []
    for admin in admins:
        sent = send_email(
            subject=f"Placement Portal — Monthly Report ({period_label})",
            to=admin.email,
            html_body=html_body,
            mail_server=current_app.config["MAIL_SERVER"],
            mail_port=current_app.config["MAIL_PORT"],
            mail_username=current_app.config["MAIL_USERNAME"],
            mail_password=current_app.config["MAIL_PASSWORD"],
            mail_use_tls=current_app.config["MAIL_USE_TLS"],
            mail_default_sender=current_app.config["MAIL_DEFAULT_SENDER"],
        )
        results.append({"admin_email": admin.email, "sent": sent})

    logger.info("Monthly report for %s sent to %s admin(s).", period_label, len(admins))
    return {"period": period_label, "results": results}


# ---------------------------------------------------------------------------
# c) User-triggered async CSV export -> file + email alert
# ---------------------------------------------------------------------------
@celery.task(name="tasks.export_applications_csv_task", bind=True)
def export_applications_csv_task(self, student_id):
    """
    Exports a student's full application history to CSV, saves it under
    EXPORT_FOLDER, and emails the student an alert once it's ready
    (with the CSV attached). Triggered from the student dashboard's
    "Export as CSV" action; runs as a background batch job via Celery.
    """
    student = Student.query.get(student_id)
    if not student:
        return {"status": "error", "message": "Student not found"}

    applications = (
        Application.query.filter_by(student_id=student.id)
        .order_by(Application.applied_on.desc())
        .all()
    )

    export_folder = current_app.config["EXPORT_FOLDER"]
    os.makedirs(export_folder, exist_ok=True)
    filename = f"applications_{student.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"
    filepath = os.path.join(export_folder, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            ["Student ID", "Company Name", "Drive Title", "Application Status", "Applied On", "Interview Date"]
        )
        for a in applications:
            drive = a.drive
            company_name = drive.company.name if drive and drive.company else ""
            writer.writerow(
                [
                    student.id,
                    company_name,
                    drive.job_title if drive else "",
                    a.status,
                    a.applied_on.strftime("%Y-%m-%d %H:%M") if a.applied_on else "",
                    a.interview_datetime.strftime("%Y-%m-%d %H:%M") if a.interview_datetime else "",
                ]
            )

    # Notify the student their export is ready
    if student.user:
        send_email(
            subject="Your Placement Portal application export is ready",
            to=student.user.email,
            html_body=(
                f"<p>Hi {student.name},</p>"
                f"<p>Your placement application history export "
                f"({len(applications)} record(s)) is ready and attached to this email.</p>"
            ),
            mail_server=current_app.config["MAIL_SERVER"],
            mail_port=current_app.config["MAIL_PORT"],
            mail_username=current_app.config["MAIL_USERNAME"],
            mail_password=current_app.config["MAIL_PASSWORD"],
            mail_use_tls=current_app.config["MAIL_USE_TLS"],
            mail_default_sender=current_app.config["MAIL_DEFAULT_SENDER"],
            attachment_path=filepath,
            attachment_name=filename,
        )

    return {
        "status": "completed",
        "student_id": student.id,
        "row_count": len(applications),
        "file": filename,
    }
