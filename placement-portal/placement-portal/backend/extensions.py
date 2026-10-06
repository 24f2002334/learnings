"""
Central location for Flask extension instances.

Kept separate from app.py to avoid circular imports: models.py, api/*.py,
and tasks.py all need `db` (and some need `cache`), and app.py needs to
import models/blueprints. Instantiating extensions here lets everyone
import from `extensions` without importing `app`.
"""
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from celery import Celery

db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()

# Celery instance is created here with a placeholder broker; it is
# reconfigured with the real app config inside app.py's make_celery().
celery = Celery(__name__)
