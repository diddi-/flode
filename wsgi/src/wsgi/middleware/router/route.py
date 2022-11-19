from typing import ParamSpec, TypeVar, Callable, List, Optional

from wsgi.http_method import HttpMethod
from wsgi.middleware.endpoint.endpoint_result import EndpointResult
from wsgi.route_pattern import RoutePattern

R = TypeVar("R", bound=EndpointResult)
P = ParamSpec("P")


class Route:
    ROUTE_ATTR = "__WSGI_ROUTE__"
    def __init__(self, path: str = "", http_methods: Optional[List[HttpMethod]] = None):
        self._path = RoutePattern(path)
        self._http_methods: List[HttpMethod] = http_methods if http_methods else [HttpMethod.GET]

    def __call__(self, method: Callable[P, R]) -> Callable[P, R]:
        setattr(method, self.ROUTE_ATTR, self)
        return method

    @property
    def path(self) -> RoutePattern:
        return self._path

    @property
    def http_methods(self) -> List[HttpMethod]:
        return self._http_methods
