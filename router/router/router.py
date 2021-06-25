# pylint: disable=no-self-use,missing-function-docstring,unused-argument
import functools
from http import HTTPStatus

from flask import Blueprint, Response
from flask import current_app as app
from flask import jsonify, request
from flask.views import MethodView
from webargs.flaskparser import abort, parser, use_args

from router.router.handlers import Headers, verify
from router.middleware import Dispatcher

router = Blueprint("router", __name__)


class Health(MethodView):
    """Health endpoint."""

    def get(self) -> Response:
        return "Healthy", HTTPStatus.OK.value


headers = functools.partial(use_args, location="headers")


class Router(MethodView):
    """Webhook router endpoint."""

    @headers(Headers())
    def post(self, hdata) -> Response:
        data = request.get_data()

        if not verify(data, hdata["x_shopify_hmac_sha256"]):
            app.logger.warning("Unauthorized connection.")
            return "Unauthorized", HTTPStatus.UNAUTHORIZED.value

        if hdata["x_shopify_test"]:
            app.logger.info("Test webhook received.")

        Dispatcher().run()

        return "Verified", HTTPStatus.OK.value


@parser.error_handler
def handle_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """Handle request errors."""
    app.logger.error(f"Error while receiving webhook: {err.messages}")
    return abort(jsonify(err.messages), HTTPStatus.UNPROCESSABLE_ENTITY.value)


# Routing
router.add_url_rule("/", view_func=Health.as_view("health"))
router.add_url_rule("/router", view_func=Router.as_view("router"))
