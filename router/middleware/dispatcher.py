from router.tasks import Processor


class Dispatcher:
    """Dispatch the webhooks to a background task processor.

    The list of all webhook events can be found at:
    https://help.shopify.com/en/api/reference/events/webhook
    """

    def __init__(self):
        ...

    def run(self):
        Processor().delay()
