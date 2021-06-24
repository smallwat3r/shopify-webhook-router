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
    SHOPIFY_SUPPORTED_API_VERSIONS = os.getenv("SHOPIFY_SUPPORTED_API_VERSION", "").split(",")


class DevelopmentConfig(DefaultConfig):
    """Default config values (development)."""


class TestConfig(DefaultConfig):
    """Testing configuration (testing)."""

    TESTING = True


class ProductionConfig(DefaultConfig):
    """Production configuration (production)."""

    DEBUG = False
