import hashlib
import hmac
from base64 import b64encode as b64e

from flask import current_app as app
from webargs import ValidationError


def verify(data, hmac_header):
    """Verify a webhook."""
    digest = hmac.new(app.config["HMAC_SECRET"], data.encode(), hashlib.sha256).digest()
    computed_hmac = b64e(digest)
    return hmac.compare_digest(computed_hmac, hmac_header.encode())


class Validator:
    """Validate schema content."""

    @classmethod
    def shop(cls, domain):
        """Validate Shopify domain."""
        if domain not in app.config["SHOPIFY_DOMAIN_ALLOWLIST"]:
            raise ValidationError(f"Domain {domain} is not allowed.")

    @classmethod
    def api(cls, version):
        """Validate that the Shopify API version is supported."""
        if version not in app.config["SHOPIFY_SUPPORTED_API_VERSIONS"]:
            raise ValidationError(f"Webhook API version {version} not supported.")
