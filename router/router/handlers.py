import hashlib
import hmac
from base64 import b64encode as b64e

from flask import current_app as app
from marshmallow import Schema, fields, validate

from router.config import SHOPIFY_DOMAIN_ALLOWLIST, SHOPIFY_SUPPORTED_API_VERSIONS


def verify(data, hmac_header):
    """Verify a webhook."""
    digest = hmac.new(app.config["HMAC_SECRET"].encode(), data, hashlib.sha256).digest()
    computed_hmac = b64e(digest)
    return hmac.compare_digest(computed_hmac, hmac_header.encode())


class Headers(Schema):
    """Expected request headers."""

    content_type = fields.Str(
        required=True,
        data_key="Content-Type",
        validate=validate.Equal("application/json"),  # does not support XML
    )
    topic = fields.Str(required=True, data_key="X-Shopify-Topic")
    hmac_sha256 = fields.Str(required=True, data_key="X-Shopify-Hmac-Sha256")
    shop = fields.Str(
        required=True,
        data_key="X-Shopify-Shop-Domain",
        validate=validate.OneOf(SHOPIFY_DOMAIN_ALLOWLIST),
    )
    version = fields.Str(
        required=True,
        data_key="X-Shopify-Api-Version",
        validate=validate.OneOf(SHOPIFY_SUPPORTED_API_VERSIONS),
    )
    webhook_id = fields.Str(required=True, data_key="X-Shopify-Webhook-Id")
    test = fields.Str(data_key="X-Shopify-Test")
