import os

from router.entrypoint import celery, create_app  # pylint: disable=unused-import

app = create_app(os.environ.get("FLASK_ENV", "production"))
app.app_context().push()
