import enum
import os


class EnvConfig(enum.Enum):
    """Environment config values."""

    TESTING = "testing"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class DefaultConfig:
    """Base config."""

    DEBUG = True
    HMAC_SECRET = os.getenv("HMAC_SECRET")

    SHOPIFY_DOMAIN_ALLOWLIST = os.getenv("SHOPIFY_DOMAIN_ALLOWLIST", "").split(",")
    SHOPIFY_SUPPORTED_API_VERSIONS = os.getenv("SHOPIFY_SUPPORTED_API_VERSIONS", "").split(",")

    REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

    CELERY_BROKER_URL = f"redis://{REDIS_HOSTNAME}:{REDIS_PORT}/0"


class DevelopmentConfig(DefaultConfig):
    """Default config values (development)."""


class TestConfig(DefaultConfig):
    """Testing configuration (testing)."""

    TESTING = True


class ProductionConfig(DefaultConfig):
    """Production configuration (production)."""

    DEBUG = False
