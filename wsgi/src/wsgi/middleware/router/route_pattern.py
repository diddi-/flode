from __future__ import annotations

import re
from typing import Any

from wsgi.middleware.router.exceptions.invalid_route_pattern_exception import InvalidRoutePatternException


class RoutePattern:
    _PATTERN_REGEX = re.compile(r"^[-/A-Za-z0-9_]+$")
    def __init__(self, pattern: str):
        if len(pattern) and not self._PATTERN_REGEX.match(pattern):
            raise InvalidRoutePatternException(pattern)
        self._raw_pattern = pattern.removesuffix("/")

    def __str__(self) -> str:
        return self._raw_pattern

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RoutePattern) and self._raw_pattern == other._raw_pattern

    def __add__(self, other: RoutePattern) -> RoutePattern:
        other_pattern = other._raw_pattern.removeprefix("/")
        return RoutePattern(self._raw_pattern + "/" + other_pattern)

    def matches(self, url_path: str) -> bool:
        if self._raw_pattern == url_path \
                or (self._raw_pattern == "" and url_path == "/"):
            return True

        return False

    def __repr__(self) -> str:
        return f"<{self.__name__}: {self._raw_pattern}>"
