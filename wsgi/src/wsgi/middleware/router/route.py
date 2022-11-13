from typing import ParamSpec, TypeVar, Callable

from wsgi.controller.controller_result import ControllerResult
from wsgi.route_template import RouteTemplate

R = TypeVar("R", bound=ControllerResult)
P = ParamSpec("P")


class Route:
    PATH_ATTR = "__WSGI_ROUTE_PATH__"
    def __init__(self, path: str = ""):
        self._path = path

    def __call__(self, method: Callable[P, R]) -> Callable[P, R]:
        setattr(method, self.PATH_ATTR, RouteTemplate(self._path))
        return method
