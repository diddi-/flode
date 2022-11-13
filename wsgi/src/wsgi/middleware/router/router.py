import inspect
from typing import Dict, Type, List

from wsgi.controller.controller import Controller
from wsgi.http_context import HttpContext
from wsgi.http_status import HttpStatus
from wsgi.middleware.endpoint.endpoint import Endpoint
from wsgi.middleware.middleware import Middleware
from wsgi.middleware.router.route import Route
from wsgi.route_template import RouteTemplate


class RouterOptions:
    def __init__(self) -> None:
        self.endpoints: Dict[str, Type[Controller]] = {}

    def add_controller(self, base_path: str, controller: Type[Controller]) -> None:
        self.endpoints[base_path] = controller


class Router(Middleware[RouterOptions]):
    OPTS: RouterOptions = RouterOptions

    def __init__(self, options: RouterOptions) -> None:
        super().__init__()
        self._endpoints: Dict[RouteTemplate, Endpoint] = {}

        for path, controller in options.endpoints.items():
            self.add_controller(path, controller)

    def handle_request(self, context: HttpContext) -> None:
        endpoint = self._endpoints.get(context.request.path, None)
        if not endpoint:
            context.response.status = HttpStatus.NOT_FOUND
            return

        context.set_endpoint(endpoint)
        self.next(context)

    def add_controller(self, base_path: str, controller: Type[Controller]) -> None:
        controller_path = RouteTemplate(base_path)
        for name, member in inspect.getmembers(controller):
            if inspect.isfunction(member) and hasattr(member, Route.PATH_ATTR):
                full_path = controller_path + getattr(member, Route.PATH_ATTR)
                self._endpoints[full_path] = Endpoint(controller, name)

    def get_routes(self) -> List[RouteTemplate]:
        return list(self._endpoints.keys())
