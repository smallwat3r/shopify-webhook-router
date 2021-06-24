import logging

from celery import Celery
from flask import Flask

from router.config import DefaultConfig, EnvConfig
from router.router.router import router
from router.tasks import Processor

celery = Celery(__name__, broker=DefaultConfig.CELERY_BROKER_URL)  # default
celery.tasks.register(Processor())


def create_app(env):
    """Application factory."""
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [sev %(levelno)s] [%(levelname)s] [%(name)s]> %(message)s",
        datefmt="%a, %d %b %Y %H:%M:%S",
    )

    if env == EnvConfig.TESTING.value:
        logging.getLogger("app").setLevel(logging.CRITICAL)

    app = Flask(__name__)

    configurations = {
        EnvConfig.TESTING.value: "router.config.TestConfig",
        EnvConfig.DEVELOPMENT.value: "router.config.DevelopmentConfig",
        EnvConfig.PRODUCTION.value: "router.config.ProductionConfig",
    }
    app.config.from_object(configurations.get(env, "router.config.ProductionConfig"))

    celery.conf.update(app.config)  # Overwrite celery default settings

    with app.app_context():
        register_blueprints(app)

    return app


def register_blueprints(app):
    """Register application blueprints."""
    app.register_blueprint(router)
