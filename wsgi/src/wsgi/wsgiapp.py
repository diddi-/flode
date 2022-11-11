from typing import List
from wsgiref.simple_server import make_server

from wsgi.http_context import HttpContext
from wsgi.http_method import HttpMethod
from wsgi.http_request import HttpRequest
from wsgi.middleware.endpoint.endpoint_middleware import EndpointMiddleware
from wsgi.middleware.middleware import Middleware
from wsgi.route_template import RouteTemplate


class WsgiApplication:
    def __init__(self):
        self._middlewares: List[Middleware] = []

    def __call__(self, environ, start_response):
        request = HttpRequest(RouteTemplate(environ["PATH_INFO"]), HttpMethod(environ["REQUEST_METHOD"]))
        context = HttpContext(request)
        # EndpointMiddleware *must* be the last one, so we're adding it here.
        self.add_middleware(EndpointMiddleware())
        # Each middleware will call the next one, so we only need to call the first.
        self._middlewares[0].handle_request(context)

        start_response(f"{context.response.status.code} {context.response.status.reason}",
                       context.response.headers.as_wsgi())
        yield context.response.body.encode("utf-8")

    def add_middleware(self, middleware: Middleware):
        if self._middlewares:
            previous = self._middlewares[-1]
            previous.next_middleware = middleware
        self._middlewares.append(middleware)

    def run_develop(self, port: int = 8000) -> None:
        with make_server("localhost", port, self) as httpd:
            print(f"Serving on localhost:{port}...")
            httpd.serve_forever()
