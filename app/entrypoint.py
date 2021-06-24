import logging

from flask import Flask

from app.api import api
from app.config import EnvConfig


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
        EnvConfig.TESTING.value: "app.config.TestConfig",
        EnvConfig.DEVELOPMENT.value: "app.config.DevelopmentConfig",
        EnvConfig.PRODUCTION.value: "app.config.ProductionConfig",
    }
    app.config.from_object(configurations.get(env, "app.config.ProductionConfig"))

    with app.app_context():
        register_blueprints(app)

    return app


def register_blueprints(app):
    """Register application blueprints."""
    app.register_blueprint(api)
