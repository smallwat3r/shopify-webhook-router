# shopify-webhook-router  

Boilerplate code to handle and process Shopify webhooks with Flask and Celery.  

**Please note this project is still under development and the current implementation might change. If you encounter any issues, please open an issue [here](https://github.com/smallwat3r/shopify-webhook-router/issues),
PRs are also more than welcome!**

## Set-up

Create a `dev.local` environment file from the template example.

``` sh
cp environments/dev.local.template environments/dev.local
```

In this file, you will need to input some info related to your Shopify store:

``` text
# environments/dev.local

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

The application provides two endpoints:
- `/`: Used for healthchecks
- `/router`: The webhooks entrypoint

## Implement your custom business logic

The webhooks must target the `https://<host>/router` endpoint.  

You can implement your own event business logic from the [Implementation](https://github.com/smallwat3r/shopify-webhook-router/blob/master/router/implementation/implementation.py) class.

Create new methods from the webhook topic names, by replacing any `/` by `_`:
- `products/create` becomes `products_create`
- `orders/partially_fulfilled` becomes `orders_partially_fulfilled`
- ...

Each methods need to implement one mandatory parameter representing a dataclass of
type `Event` from which you can get the following attributes:

- `data`: the webhook data (`dict`)
- `topic`: the topic name (`str`)
- `shop`: the Shopify shop domain (`str`)
- `version`: the webhook API version (`str`)
- `webhook_id`: the unique webhook_id (`str`)
- `test`: a flag used to spot test Shopify webhooks (`bool`)

``` python
@dataclass
class Event:

    data: dict
    topic: str
    shop: str
    version: str
    webhook_id: str
    test: bool
```

#### Implementation example:  

``` python
# router/implementation/implementation.py
from router.event import Event


class Implementation:
 
    # (...)
    
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

```

Any topic events received for non-existant methods will raise a `NotImplemented` exception.  

The list of all webhook topics can be found [here](https://help.shopify.com/en/api/reference/events/webhook)  
