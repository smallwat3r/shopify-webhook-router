from router.event import Event
from router.implementation.implementation import Implementation


def dispatch(event: Event):
    """Dispatch the webhooks events to their related topic handler."""
    try:
        getattr(Implementation(), event.topic.replace("/", "_"))(event)
    except AttributeError as err:
        raise NotImplementedError(f"Topic {event.topic} not implemented") from err
