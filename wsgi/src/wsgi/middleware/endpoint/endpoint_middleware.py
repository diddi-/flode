from wsgi.http_context import HttpContext
from wsgi.middleware.middleware import Middleware


class EndpointMiddleware(Middleware):
    def __init__(self):
        super().__init__()

    def handle_request(self, context: HttpContext) -> None:
        endpoint = context.get_endpoint()
        controller = endpoint.controller(context.request)
        method = getattr(controller, endpoint.method_name)
        body = method()
        context.response.body = body
        # This middleware *should* be last but we want to play nice just in case.
        self.next(context)
