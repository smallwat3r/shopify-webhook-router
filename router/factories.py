from flask import Flask

from router.config import Environment
from router.extensions import celery
from router.router.router import router


def make_celery(app: Flask):
    """Configure Celery from the application factory."""

    class ContextTask(celery.Task):  # pylint: disable=missing-class-docstring
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"])
    celery.Task = ContextTask

    return celery


def create_app(env=Environment.PRODUCTION.value):
    """Application factory."""
    app = Flask(__name__)

    configurations = {
        Environment.TESTING.value: "router.config.TestConfig",
        Environment.DEVELOPMENT.value: "router.config.DevelopmentConfig",
        Environment.PRODUCTION.value: "router.config.ProductionConfig",
    }
    app.config.from_object(configurations.get(env, "router.config.ProductionConfig"))

    celery.conf.update(broker_url=app.config["CELERY_BROKER_URL"])

    with app.app_context():
        app.register_blueprint(router)

    return app
