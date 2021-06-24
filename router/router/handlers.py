import hashlib
import hmac
from base64 import b64encode as b64e

from flask import current_app as app
from marshmallow import Schema, ValidationError, fields


def verify(data, hmac_header):
    """Verify a webhook."""
    digest = hmac.new(app.config["HMAC_SECRET"].encode(), data, hashlib.sha256).digest()
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


class Headers(Schema):
    """Expected request headers."""

    x_shopify_topic = fields.Str(required=True, data_key="X-Shopify-Topic")
    x_shopify_hmac_sha256 = fields.Str(required=True, data_key="X-Shopify-Hmac-Sha256")
    x_shopify_shop_domain = fields.Str(
        required=True, data_key="X-Shopify-Shop-Domain", validate=Validator.shop
    )
    x_shopify_api_version = fields.Str(
        required=True, data_key="X-Shopify-Api-Version", validate=Validator.api
    )
    x_shopify_webhook_id = fields.Str(required=True, data_key="X-Shopify-Webhook-Id")
    x_shopify_test = fields.Str(data_key="X-Shopify-Test")
