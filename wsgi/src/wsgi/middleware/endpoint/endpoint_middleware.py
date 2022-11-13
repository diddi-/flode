from typing import cast

from wsgi.controller.controller_result import ControllerResult
from wsgi.http_context import HttpContext
from wsgi.middleware.middleware import Middleware
from wsgi.middleware.no_options import NoOptions


class EndpointMiddleware(Middleware[NoOptions]):
    def handle_request(self, context: HttpContext) -> None:
        endpoint = context.get_endpoint()
        controller = endpoint.controller()
        controller.request = context.request
        method = getattr(controller, endpoint.method_name)

        # NOTE: This needs better checking of the return type at runtime but also ensure static typing works.
        result = cast(ControllerResult, method())
        context.response.body = result.content
        context.response.status = result.status
        # This middleware *should* be last but we want to play nice just in case.
        self.next(context)
