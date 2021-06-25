from dataclasses import dataclass


@dataclass
class Event:
    """Webhook event dataclass."""

    data: dict
    topic: str
    shop: str
    version: str
    webhook_id: str
    test: bool
