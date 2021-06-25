import os

from router.factories import create_app, make_celery

celery = make_celery(create_app(os.getenv("FLASK_ENV")))
