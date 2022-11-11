from typing import ParamSpec, TypeVar, Callable

from wsgi.route_template import RouteTemplate

R = TypeVar("R")
P = ParamSpec("P")


class Route:
    def __init__(self, path: str):
        self._path = path

    def __call__(self, method: Callable[P, R]) -> Callable[P, R]:
        method.path = RouteTemplate(self._path)
        return method
