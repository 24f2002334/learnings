import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

    # --- Database (SQLite, programmatically created) ---
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        BASE_DIR, "instance", "placement_portal.sqlite3"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- JWT ---
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)
    JWT_TOKEN_LOCATION = ["headers"]

    # --- Redis / Cache ---
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    CACHE_DEFAULT_TIMEOUT = 60  # seconds

    # --- Celery ---
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/1")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/2"
    )

    # --- File uploads ---
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "resumes")
    EXPORT_FOLDER = os.path.join(BASE_DIR, "uploads", "exports")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5 MB
    ALLOWED_RESUME_EXTENSIONS = {"pdf", "doc", "docx"}

    # --- Admin bootstrap (used only by seed.py, not a registration route) ---
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@placementportal.local")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@123")
    ADMIN_NAME = os.environ.get("ADMIN_NAME", "Placement Cell Admin")

    # --- Google Chat webhook (daily reminders) ---
    GCHAT_WEBHOOK_URL = os.environ.get("GCHAT_WEBHOOK_URL", "")

    # --- SMTP (monthly report email) ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "")

    # --- Celery Beat schedule ---
    # Daily reminder time (24h, server local/UTC time) and monthly report day
    REMINDER_HOUR = int(os.environ.get("REMINDER_HOUR", 9))   # 09:00
    REMINDER_MINUTE = int(os.environ.get("REMINDER_MINUTE", 0))
    REMINDER_DAYS_AHEAD = int(os.environ.get("REMINDER_DAYS_AHEAD", 3))
