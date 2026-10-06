import os
from dotenv import load_dotenv

load_dotenv()  # loads backend/.env if present; safe no-op otherwise

from flask import Flask, render_template, jsonify
from config import Config
from extensions import db, jwt, cache, celery


def make_celery(app):
    """Bind the module-level `celery` instance to this Flask app's config
    so tasks run inside the app context (needed for db access), and wire
    up the Celery Beat schedule for the two recurring jobs."""
    from celery.schedules import crontab

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        beat_schedule={
            "send-daily-deadline-reminders": {
                "task": "tasks.send_daily_deadline_reminders",
                "schedule": crontab(
                    hour=app.config["REMINDER_HOUR"], minute=app.config["REMINDER_MINUTE"]
                ),
                "kwargs": {"days_ahead": app.config["REMINDER_DAYS_AHEAD"]},
            },
            "generate-monthly-report": {
                "task": "tasks.generate_monthly_report",
                "schedule": crontab(day_of_month=1, hour=6, minute=0),
            },
        },
        timezone="UTC",
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "static"),
        static_url_path="/static",
    )
    app.config.from_object(config_class)

    os.makedirs(os.path.join(os.path.dirname(__file__), "instance"), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["EXPORT_FOLDER"], exist_ok=True)

    # --- Extensions ---
    db.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)
    make_celery(app)

    # --- Blueprints ---
    from api.auth import auth_bp
    from api.admin import admin_bp
    from api.company import company_bp
    from api.student import student_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(company_bp, url_prefix="/api/company")
    app.register_blueprint(student_bp, url_prefix="/api/student")

    # --- JWT error handlers (return clean JSON instead of HTML) ---
    @jwt.unauthorized_loader
    def unauthorized_callback(reason):
        return jsonify({"error": "Missing or invalid token", "detail": reason}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({"error": "Invalid token", "detail": reason}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"error": "Token has expired"}), 401

    # --- Frontend entry point (Jinja2 used only as a CDN shell, not for UI) ---
    @app.route("/")
    @app.route("/<path:path>")
    def index(path=None):
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
