"""
Notification helpers used by Celery tasks:
    - send_gchat_message(webhook_url, text)   -> daily reminders
    - send_email(subject, to, html_body, ...) -> monthly report, export-ready alert

Kept dependency-free (uses `requests` and Python's stdlib `smtplib`) so no
extra frameworks are pulled in beyond what's already required.
"""
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

import requests

logger = logging.getLogger(__name__)


def send_gchat_message(webhook_url, text):
    """Post a simple text message to a Google Chat space via incoming webhook.
    Returns True on success, False otherwise (never raises, so a bad/missing
    webhook doesn't crash the whole reminder task for other users)."""
    if not webhook_url:
        logger.warning("GCHAT_WEBHOOK_URL not configured; skipping chat notification.")
        return False
    try:
        resp = requests.post(webhook_url, json={"text": text}, timeout=10)
        if resp.status_code >= 300:
            logger.error("Google Chat webhook failed: %s %s", resp.status_code, resp.text)
            return False
        return True
    except requests.RequestException as exc:
        logger.error("Google Chat webhook request error: %s", exc)
        return False


def send_email(
    subject,
    to,
    html_body,
    *,
    mail_server,
    mail_port,
    mail_username,
    mail_password,
    mail_use_tls,
    mail_default_sender,
    attachment_path=None,
    attachment_name=None,
):
    """Send an HTML email, optionally with a single file attachment
    (used for the CSV export-ready notification). Returns True/False."""
    if not mail_username or not mail_password:
        logger.warning("MAIL_USERNAME/MAIL_PASSWORD not configured; skipping email to %s", to)
        return False

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = mail_default_sender or mail_username
    msg["To"] = to

    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(html_body, "html"))
    msg.attach(alt)

    if attachment_path:
        try:
            with open(attachment_path, "rb") as f:
                part = MIMEApplication(f.read(), Name=attachment_name or "attachment.csv")
            part["Content-Disposition"] = f'attachment; filename="{attachment_name}"'
            msg.attach(part)
        except OSError as exc:
            logger.error("Could not attach file %s: %s", attachment_path, exc)

    try:
        with smtplib.SMTP(mail_server, mail_port, timeout=15) as server:
            if mail_use_tls:
                server.starttls()
            server.login(mail_username, mail_password)
            server.sendmail(msg["From"], [to], msg.as_string())
        return True
    except (smtplib.SMTPException, OSError) as exc:
        logger.error("Failed to send email to %s: %s", to, exc)
        return False
