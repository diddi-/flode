import inspect
from typing import Dict, Type, List

from wsgi.di.container import Container
from wsgi.di.provider.lifetime import Lifetime
from wsgi.endpoint.controller import Controller
from wsgi.http_context import HttpContext
from wsgi.http_status import HttpStatus
from wsgi.middleware.endpoint.class_endpoint import ClassEndpoint
from wsgi.middleware.middleware import Middleware
from wsgi.middleware.router.route import Route
from wsgi.middleware.router.router_options import RouterOptions
from wsgi.route_template import RouteTemplate


class Router(Middleware[RouterOptions]):
    _OPTS = RouterOptions

    def __init__(self, options: RouterOptions, container: Container) -> None:
        super().__init__()
        self._endpoints: Dict[RouteTemplate, ClassEndpoint] = {}
        self._container = container

        for path, controller in options.endpoints.items():
            self.add_controller(path, controller)

    def handle_request(self, context: HttpContext) -> None:
        endpoint = self._endpoints.get(context.request.path, None)
        if not endpoint:
            context.response.status = HttpStatus.NOT_FOUND
            return

        controller = self._container.get_service(endpoint.controller)
        context.set_endpoint(getattr(controller, endpoint.method_name))
        self.next(context)

    def add_controller(self, base_path: str, controller: Type[Controller]) -> None:
        self._container.register(controller, lifetime=Lifetime.SINGLETON)
        controller_path = RouteTemplate(base_path)
        for name, member in inspect.getmembers(controller):
            if inspect.isroutine(member) and hasattr(member, Route.PATH_ATTR):
                full_path = controller_path + getattr(member, Route.PATH_ATTR)
                self._endpoints[full_path] = ClassEndpoint(controller, name)

    def get_routes(self) -> List[RouteTemplate]:
        return list(self._endpoints.keys())
