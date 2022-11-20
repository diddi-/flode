from __future__ import annotations

from typing import Optional

from flode.http_context import HttpContext
from flode.http_method import HttpMethod
from flode.http_request import HttpRequest
from flode.middleware.router.url_path import UrlPath


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
        request = HttpRequest(UrlPath(self._path), self._method)
        return HttpContext(request)
