# pylint: disable=no-self-use,missing-function-docstring,unused-argument
import functools
from datetime import datetime
from http import HTTPStatus

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, request
from flask.views import MethodView
from webargs.flaskparser import abort, parser, use_kwargs

from router.extensions import redis_client
from router.router.helpers import Headers, verify
from router.tasks import Processor

router = Blueprint("router", __name__)
headers = functools.partial(use_kwargs, location="headers")


class Health(MethodView):
    """Health endpoint."""

    def get(self):
        return "Healthy", HTTPStatus.OK.value


class Router(MethodView):
    """Webhook router endpoint."""

    @headers(Headers())
    def post(self, topic, shop, version, webhook_id, hmac_sha256, test=False, **kwargs):
        data = request.get_data()

        if not verify(data, hmac_sha256):
            app.logger.error(f"{webhook_id} {topic} unauthorized connection")
            return "Unauthorized", HTTPStatus.UNAUTHORIZED.value

        if test:
            app.logger.info(f"*TEST* {webhook_id} {topic} received")

        if date_seen := redis_client.get(webhook_id):
            app.logger.warning(f"{webhook_id} {topic} already seen on {date_seen.decode()}")
        else:
            Processor().delay(data.decode(), topic, shop, version, webhook_id, test)
            redis_client.set(webhook_id, str(datetime.now()))
            app.logger.info(f"{webhook_id} {topic} received")

        return "Verified", HTTPStatus.OK.value


@parser.error_handler
def handle_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """Handle request errors."""
    app.logger.error(f"Error while receiving webhook: {err.messages}")
    return abort(jsonify(err.messages), HTTPStatus.UNPROCESSABLE_ENTITY.value)


# Routing
router.add_url_rule("/", view_func=Health.as_view("health"))
router.add_url_rule("/router", view_func=Router.as_view("router"))
