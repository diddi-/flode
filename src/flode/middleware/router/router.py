import inspect
from typing import Type, List, cast

from flode.di.container import Container
from flode.di.provider.lifetime import Lifetime
from flode.http_context import HttpContext
from flode.http_status import HttpStatus
from flode.middleware.endpoint.class_endpoint import ClassEndpoint
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
        controller = self._container.get_service(endpoint.controller)
        context.set_endpoint(getattr(controller, endpoint.method_name))
        self.next(context)

    def add_endpoint(self, base_path: str, controller: Type[object]) -> None:
        self._container.register(controller, lifetime=Lifetime.SINGLETON)
        controller_path = RoutePattern(base_path)
        for name, member in inspect.getmembers(controller):
            if inspect.isroutine(member) and hasattr(member, Route.ROUTE_ATTR):
                route = cast(Route, getattr(member, Route.ROUTE_ATTR))
                full_path = controller_path + route.pattern
                self._endpoints.add(ClassEndpoint(controller, name, Route(str(full_path), route.http_methods)))

    def get_routes(self) -> List[RoutePattern]:
        return self._endpoints.get_all_routes()
