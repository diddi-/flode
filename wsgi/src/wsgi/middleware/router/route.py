from typing import ParamSpec, TypeVar, Callable

from wsgi.controller.controller_result import ControllerResult
from wsgi.route_template import RouteTemplate

R = TypeVar("R", bound=ControllerResult)
P = ParamSpec("P")


class Route:
    def __init__(self, path: str = ""):
        self._path = path

    def __call__(self, method: Callable[P, R]) -> Callable[P, R]:
        setattr(method, "path", RouteTemplate(self._path))
        return method
