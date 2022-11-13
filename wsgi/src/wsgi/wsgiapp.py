from typing import List, Iterator, Dict, Any
from wsgiref.simple_server import make_server

from wsgi.di.container import Container
from wsgi.http_context import HttpContext
from wsgi.http_method import HttpMethod
from wsgi.http_request import HttpRequest
from wsgi.http_response import HttpResponse
from wsgi.middleware.endpoint.endpoint_middleware import EndpointMiddleware
from wsgi.middleware.middleware import Middleware
from wsgi.middleware.router.router import Router
from wsgi.route_template import RouteTemplate


class WsgiApplication:
    def __init__(self) -> None:
        self._middlewares: List[Middleware] = []
        self._container = Container()

    # start_response from wsgi spec is very strange. There is no annotations for it and no type hinting on earth will
    # satisfy mypy. We could import wsgiref.type.StartResponse which will make mypy happy but that fails at runtime
    # because wsgiref.type is not available then... This will be ignored for now.
    def __call__(self, environ: Dict[str, Any], start_response) -> Iterator[bytes]:  # type: ignore
        request = HttpRequest(RouteTemplate(environ["PATH_INFO"]), HttpMethod(environ["REQUEST_METHOD"]))
        response = self._handle_request(request)
        start_response(f"{response.status.code} {response.status.reason}",
                       response.headers.as_wsgi())
        yield response.body.encode("utf-8")

    def _handle_request(self, request: HttpRequest) -> HttpResponse:
        context = HttpContext(request)
        # EndpointMiddleware *must* be the last one, so we're adding it here.
        self.add_middleware(EndpointMiddleware())
        # Each middleware will call the next one, so we only need to call the first.
        self._middlewares[0].handle_request(context)
        return context.response

    def add_middleware(self, middleware: Middleware) -> None:
        if self._middlewares:
            previous = self._middlewares[-1]
            previous.next_middleware = middleware
        self._middlewares.append(middleware)

    def run_develop(self, port: int = 8000) -> None:
        print("Running in DEVELOPMENT mode")
        with make_server("localhost", port, self) as httpd:
            print(f"Serving on localhost:{port}...")
            httpd.serve_forever()

    def get_routes(self) -> List[RouteTemplate]:
        for mw in self._middlewares:
            if isinstance(mw, Router):
                return mw.get_routes()
        return []
