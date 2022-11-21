from typing import cast

from flode.di.container import Container
from flode.middleware.endpoint.endpoint_result import EndpointResult
from flode.http_context import HttpContext
from flode.middleware.middleware import Middleware
from flode.middleware.no_options import NoOptions


class EndpointMiddleware(Middleware[NoOptions]):
    """ This class is responsible for calling the endpoint registered for a specific path.
        This will *always* be the last middleware in the chain. """

    def __init__(self, container: Container) -> None:
        super().__init__()
        self._container = container

    def handle_request(self, context: HttpContext) -> None:
        endpoint = context.get_endpoint()

        # NOTE: This needs better checking of the return type at runtime but also ensure static typing works.
        result = cast(EndpointResult, self._container.invoke(endpoint.fn))
        context.response.body = result.content
        context.response.status = result.status
