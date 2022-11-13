from typing import Optional, TypeVar, Callable

from wsgi.http_request import HttpRequest
from wsgi.http_response import HttpResponse

R = TypeVar("R")


class HttpContext:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.response = HttpResponse()

        # Unfortunately MyPy doesn't seem to support ParamSpec here yet so using '...' instead.
        self._endpoint: Optional[Callable[..., R]] = None

    def set_endpoint(self, endpoint: Callable[..., R]) -> None:
        self._endpoint = endpoint

    def get_endpoint(self) -> Callable[..., R]:
        if not self._endpoint:
            raise ValueError("No endpoint set!")

        return self._endpoint
