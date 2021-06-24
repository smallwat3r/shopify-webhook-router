# pylint: disable=no-self-use,missing-function-docstring,unused-argument
import functools
from http import HTTPStatus

from flask import Blueprint, Response, abort
from flask import current_app as app
from flask import jsonify, make_response, request
from flask.views import MethodView
from webargs.flaskparser import parser, use_args

from router.router.handlers import verify
from router.router.schemas import Headers

router = Blueprint("router", __name__)

headers = functools.partial(use_args, location="headers")


class Health(MethodView):
    """Health endpoint."""

    def get(self) -> Response:
        return "Healthy", HTTPStatus.OK.value


class Router(MethodView):
    """Webhook receiver endpoint."""

    @headers(Headers())
    def post(self, hdata) -> Response:
        data = request.get_data()

        if not verify(data, hdata["x_shopify_hmac_sha256"]):
            app.logger.warning("Unauthorized connection.")
            return abort(401)

        if hdata["x_shopify_test"]:
            app.logger.info("Test webhook received.")

        return "Verified", HTTPStatus.OK.value


@parser.error_handler
def handle_parsing_error(err, req, schema, *, error_status_code, error_headers):
    """Handle request errors."""
    app.logger.error(err.messages)
    return make_response(jsonify(err.messages), HTTPStatus.UNPROCESSABLE_ENTITY.value)


# Routing
router.add_url_rule("/", view_func=Health.as_view("health"))
router.add_url_rule("/router", view_func=Router.as_view("webhook"))
