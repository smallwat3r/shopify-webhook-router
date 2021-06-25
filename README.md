# shopify-webhook-router  

Boilerplate code to handle and process Shopify webhooks with Flask and Celery.  

**Please note this project is still under development and the current implementation might change.  
If you encounter any issues, please open an issue [here](https://github.com/smallwat3r/shopify-webhook-router/issues),
PRs are also more than welcome!**

## Set-up

Create a `dev.local` environment file from the template example.

``` sh
cp environment/dev.local.template environment/dev.local
```

In this file, you will need to input some info related to your Shopify store:

``` text
# environment/dev.local

FLASK_ENV=development
FLASK_DEBUG=1

# Signed Shopify secret used to verify the webhooks
HMAC_SECRET=<secret>

# Comma separated lists
SHOPIFY_DOMAIN_ALLOWLIST=<domain.myshopify.com>
SHOPIFY_SUPPORTED_API_VERSIONS=2021-04,2021-07

REDIS_HOSTNAME=localhost
REDIS_PORT=6379
```

Start a local instance of Redis from docker:

``` sh
docker run -d -p 6379:6379 redis
```

Start a local instance of the Flask app:
``` sh
make local
```

Start a local instance of Celery:
``` sh
make worker
```

You can use ngrok to get a temporary https endpoint to test the webhook behaviour
between Shopify and your local app:  

``` sh
ngrok http 5000
```

## Implement your custom business logic

You can implement your own event business logic from the [Implementation](https://github.com/smallwat3r/shopify-webhook-router/blob/master/router/implementation/implementation.py) class.

Create new methods from the webhook topic names, by replacing the `/` by `_`:
- `products/create` becomes `products_create`
- `orders/partially_fulfilled` becomes `orders_partially_fulfilled`
- ...

Each methods needs to implement these mandatory parameters:  
- `data`: The dictionary of data related to the event.
- `shop`: The webhook shop domain name.
- `version`: The webhook API version used.
- `webhook_id`: The unique webhook id.
- `test`: Boolean flag to spot test Shopify webhooks.

Example:  

``` python
# router/implementation/implementation.py

class Implementation:
    
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

```

Any events received for non-implemented methods will raise a `NotImplemented` exception.  

The list of all webhook topics can be found [here](https://help.shopify.com/en/api/reference/events/webhook)  
