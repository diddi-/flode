from __future__ import annotations

from typing import Optional

from wsgi.http_context import HttpContext
from wsgi.http_method import HttpMethod
from wsgi.http_request import HttpRequest


class HttpContextBuilder:

    def __init__(self) -> None:
        self._path: Optional[str] = None
        self._method: HttpMethod = HttpMethod.GET

    def path(self, path: str) -> HttpContextBuilder:
        self._path = path
        return self

    def http_method(self, http_method: HttpMethod) -> HttpContextBuilder:
        self._method = http_method
        return self

    def build(self) -> HttpContext:
        if not self._path:
            raise ValueError("HttpContext require a route path")
        request = HttpRequest(self._path, self._method)
        return HttpContext(request)
