from marshmallow import Schema, fields

from app.api.handlers import Validator


class Headers(Schema):
    """Expected request headers."""

    x_shopify_topic = fields.Str(required=True, data_key="X-Shopify-Topic")
    x_shopify_hmac_sha256 = fields.Str(required=True, data_key="X-Shopify-Hmac-Sha256")
    x_shopify_shop_domain = fields.Str(
        required=True, data_key="X-Shopify-Shop-Domain", validate=Validator.shop
    )
    x_shopify_api_version = fields.Str(
        required=True, data_key="X-Shopify-API-Version", validate=Validator.api
    )
    x_shopify_webhook_id = fields.Str(required=True, data_key="X-Shopify-Webhook-Id")
    x_shopify_test = fields.Str(data_key="X-Shopify-Test")
