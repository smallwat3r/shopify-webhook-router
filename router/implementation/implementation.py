from router.event import Event  # pylint: disable=unused-import


class Implementation:
    """Implement custom business logics from Shopify webhooks topic events.

    You can map events by creating the relative methods under this class. Just replace
    any "/" from the event topic by an "_".

    Each methods need to implement one mandatory parameter representing a dataclass of
    type `Event` from which you can get the following attributes:

        data: the webhook data (dict)
        topic: the topic name (str)
        shop: the Shopify shop domain (str)
        version: the webhook API version (str)
        webhook_id: the unique webhook_id (str)
        test: a flag used to spot test Shopify webhooks (bool)

    Any topic events received for non-existant methods will raise a `NotImplemented`
    exception.

    The list of all webhook topics can be found at:
    https://help.shopify.com/en/api/reference/events/webhook

    Example:

        class Implementation:

            # topic order/paid
            def orders_paid(self, hook: Event):
                if hook.test:
                    pass
                print(hook.shop, hook.version, hook.topic)
                data = hook.data
                order_id = data.get("order_id")
                email = data.get("email")
                # ... send order to warehouse, send confirmation email ...

            # topic order/delete
            def orders_delete(self, hook: Event):
                ...

            # topic inventory_items/create
            def inventory_items_create(self, hook: Event):
                ...

    """

    # def orders_create(self, hook: Event):
    #     print(hook.data.get("order_id"))
