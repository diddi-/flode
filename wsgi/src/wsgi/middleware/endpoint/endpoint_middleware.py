from typing import cast

from wsgi.di.container import Container
from wsgi.endpoint.endpoint_result import EndpointResult
from wsgi.http_context import HttpContext
from wsgi.middleware.middleware import Middleware
from wsgi.middleware.no_options import NoOptions


class EndpointMiddleware(Middleware[NoOptions]):
    def __init__(self, container: Container) -> None:
        super().__init__()
        self._container = container

    """ This class is responsible for calling the endpoint registered for a specific path.
        This will *always* be the last middleware in the chain. """
    def handle_request(self, context: HttpContext) -> None:
        endpoint = context.get_endpoint()

        # NOTE: This needs better checking of the return type at runtime but also ensure static typing works.
        result = cast(EndpointResult, self._container.invoke(endpoint))
        context.response.body = result.content
        context.response.status = result.status
