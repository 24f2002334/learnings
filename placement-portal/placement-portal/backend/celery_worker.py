"""
Run with:  celery -A celery_worker.celery worker --loglevel=info
(add --beat, or run `celery -A celery_worker.celery beat` separately,
once scheduled tasks are configured in the next build stage.)
"""
from app import create_app, make_celery
from extensions import celery

flask_app = create_app()
make_celery(flask_app)

# Ensure task modules are registered with this celery instance
import tasks  # noqa: E402,F401
