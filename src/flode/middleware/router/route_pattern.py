from __future__ import annotations

import re
from typing import Any, List, Dict

from flode.middleware.router.exceptions.invalid_route_pattern_exception import InvalidRoutePatternException
from flode.middleware.router.string_placeholder import StringPlaceholder
from flode.middleware.router.url_path import UrlPath


class RoutePattern:
    _PLACEHOLDER_REGEX = re.compile(r"<([a-z]+)>")
    _PATTERN_REGEX = re.compile(r"^(/([-/A-Za-z0-9_]+|<[a-z]+>)*)+$")

    def __init__(self, pattern: str):
        if not pattern.startswith("/"):
            raise InvalidRoutePatternException(f"Route patterns must begin with a '/' ({pattern})")
        if len(pattern) > 1 and pattern.endswith("/"):
            raise InvalidRoutePatternException(f"Route patterns can't end with a '/' ({pattern})")
        if not self._PATTERN_REGEX.match(pattern):
            raise InvalidRoutePatternException(f"'{pattern}' is not a valid route pattern")

        self._raw_pattern = pattern
        self._pattern_parts: List[str] = pattern.split("/")[1:]
        self._placeholders: Dict[str, StringPlaceholder] = {}  # pattern_part, Placeholder

        # I'm sure there is a better way to do this using only regex...
        index = 0
        for part in self._pattern_parts:
            match = self._PLACEHOLDER_REGEX.match(part)
            if match:
                self._placeholders[part] = StringPlaceholder(match.group(1), index)
            index += 1

    def __str__(self) -> str:
        return self._raw_pattern

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RoutePattern) and self._raw_pattern == other._raw_pattern

    def __add__(self, other: RoutePattern) -> RoutePattern:
        if len(str(other)) > 1:
            other_pattern = other._raw_pattern.removeprefix("/")
            return RoutePattern(self._raw_pattern + "/" + other_pattern)

        # 'other' may be a single '/' in which case there isn't much to concatenate.
        return RoutePattern(self._raw_pattern)

    def matches(self, url_path: UrlPath) -> bool:
        if not len(self._pattern_parts) == len(url_path):
            return False

        index = 0
        for part in self._pattern_parts:
            if placeholder := self._placeholders.get(part, None):
                if not placeholder.matches(url_path[index]):
                    return False

            elif not part == url_path[index]:
                return False
            index += 1

        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._raw_pattern}>"
