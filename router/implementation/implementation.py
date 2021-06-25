class Implementation:
    """Implement custom business logics from Shopify webhooks topic events.

    You can map events by creating the relative methods under this class. Just replace
    any "/" from the event topic by an "_".

    The list of all webhook topics can be found at:
    https://help.shopify.com/en/api/reference/events/webhook

    Example:

        # topic order/paid
        def orders_paid(self, data, shop, version, webhook_id, test):
            if test:
                pass
            order_id = data.get("order_id")
            email = data.get("email")
            # ... send order to warehouse, send confirmation email ...

        # topic order/delete
        def order_delete(self, data, shop, version, webhook_id, test):
            ...

        # topic inventory_items/create
        def inventory_items_create(self, data, shop, version, webhook_id, test):
            ...

    """
