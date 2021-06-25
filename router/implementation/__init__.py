from router.implementation.implementation import Implementation


def dispatch(data, topic, shop, version, webhook_id, test):
    """Dispatch the webhooks to their related topic handler."""
    try:
        getattr(Implementation(), topic.replace("/", "_"))(data, shop, version, webhook_id, test)
    except AttributeError as err:
        raise NotImplementedError(f"Topic {topic} not implemented") from err
