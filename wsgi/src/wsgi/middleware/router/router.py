import inspect
from typing import Dict, Type, List

from wsgi.controller.controller import Controller
from wsgi.http_context import HttpContext
from wsgi.http_status import HttpStatus
from wsgi.middleware.endpoint.endpoint import Endpoint
from wsgi.middleware.middleware import Middleware
from wsgi.route_template import RouteTemplate


class Router(Middleware):
    def __init__(self) -> None:
        super().__init__()
        self._endpoints: Dict[RouteTemplate, Endpoint] = {}

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
            if inspect.isfunction(member) and hasattr(member, "path"):
                full_path = controller_path + getattr(member, "path")
                self._endpoints[full_path] = Endpoint(controller, name)

    def get_routes(self) -> List[RouteTemplate]:
        return list(self._endpoints.keys())
