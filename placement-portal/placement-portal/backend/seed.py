"""
Creates all tables programmatically (via SQLAlchemy model metadata) and
bootstraps the single pre-existing Admin user. Run this once before first
starting the server:

    python seed.py

Re-running is safe: it will not duplicate the admin user or drop existing
data. To start completely fresh, delete backend/instance/placement_portal.sqlite3
and run this again.
"""
from app import create_app
from extensions import db
from models import User

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created (or already existed).")

    admin_email = app.config["ADMIN_EMAIL"]
    existing_admin = User.query.filter_by(role="admin").first()

    if existing_admin:
        print(f"Admin already exists: {existing_admin.email}")
    else:
        admin = User(email=admin_email, role="admin", is_active=True)
        admin.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created: {admin_email} / (password from ADMIN_PASSWORD env var or default)")

    print("Seed complete.")
