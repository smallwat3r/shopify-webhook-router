import enum
import os


class Environment(enum.Enum):
    """Environment configuration values."""

    TESTING = "testing"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class BaseConfig:
    """Base configuration."""

    DEBUG = True
    HMAC_SECRET = os.getenv("HMAC_SECRET")

    SHOPIFY_DOMAIN_ALLOWLIST = os.getenv("SHOPIFY_DOMAIN_ALLOWLIST", "").split(",")
    SHOPIFY_SUPPORTED_API_VERSIONS = os.getenv("SHOPIFY_SUPPORTED_API_VERSIONS", "").split(",")

    REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

    CELERY_BROKER_URL = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/0"


class DevelopmentConfig(BaseConfig):
    """Development configuration (development)."""


class TestConfig(BaseConfig):
    """Testing configuration (testing)."""

    TESTING = True


class ProductionConfig(BaseConfig):
    """Production configuration (production)."""

    DEBUG = False
