from typing import ParamSpec, TypeVar, Callable, List, Optional

from flode.http_method import HttpMethod
from flode.middleware.endpoint.endpoint_result import EndpointResult
from flode.middleware.router.route_pattern import RoutePattern

R = TypeVar("R", bound=EndpointResult)
P = ParamSpec("P")


class Route:
    """ A Route connects a Path with an Endpoint. It contains a  """
    ROUTE_ATTR = "__WSGI_ROUTE__"

    def __init__(self, pattern: str = "/", http_methods: Optional[List[HttpMethod]] = None):
        self._pattern = RoutePattern(pattern)
        self._http_methods: List[HttpMethod] = http_methods if http_methods else [HttpMethod.GET]

    def __call__(self, method: Callable[P, R]) -> Callable[P, R]:
        setattr(method, self.ROUTE_ATTR, self)
        return method

    @property
    def pattern(self) -> RoutePattern:
        return self._pattern

    @property
    def http_methods(self) -> List[HttpMethod]:
        return self._http_methods
