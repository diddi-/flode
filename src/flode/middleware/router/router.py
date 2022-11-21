import inspect
from typing import Type, List, cast

from flode.di.container import Container
from flode.di.provider.lifetime import Lifetime
from flode.http_context import HttpContext
from flode.http_status import HttpStatus
from flode.middleware.endpoint.endpoint import Endpoint
from flode.middleware.middleware import Middleware
from flode.middleware.router.endpoint_collection import EndpointCollection
from flode.middleware.router.route import Route
from flode.middleware.router.router_options import RouterOptions
from flode.middleware.router.route_pattern import RoutePattern


class Router(Middleware[RouterOptions]):
    _OPTS = RouterOptions

    def __init__(self, options: RouterOptions, container: Container) -> None:
        super().__init__()
        self._endpoints: EndpointCollection = EndpointCollection()
        self._container = container

        for path, controller in options.endpoints.items():
            self.add_endpoint(path, controller)

    def handle_request(self, context: HttpContext) -> None:
        if not self._endpoints.has_endpoint(context.request.path, context.request.http_method):
            context.response.status = HttpStatus.NOT_FOUND
            return

        endpoint = self._endpoints.get_endpoint(context.request.path, context.request.http_method)
        context.set_endpoint(endpoint)
        self.next(context)

    def add_endpoint(self, route_pattern: str, cls: Type[object]) -> None:
        self._container.register(cls, lifetime=Lifetime.SINGLETON)
        base_route_pattern = RoutePattern(route_pattern)
        controller = self._container.get_service(cls)
        for name, member in inspect.getmembers(controller):
            if inspect.isroutine(member) and hasattr(member, Route.ROUTE_ATTR):
                route = cast(Route, getattr(member, Route.ROUTE_ATTR))
                full_path = base_route_pattern + route.pattern
                self._endpoints.add(Endpoint(member, Route(str(full_path), route.http_methods)))

    def get_routes(self) -> List[RoutePattern]:
        return self._endpoints.get_all_routes()
