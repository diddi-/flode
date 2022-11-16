from __future__ import annotations

from typing import Any, Iterator


class RouteTemplate:
    def __init__(self, path: str):
        self._raw_path = path.removesuffix("/")

    def __getitem__(self, index: int) -> str:
        if self._raw_path.startswith("/"):
            index += 1  # split would cause first result to be empty

        return self._raw_path.split("/")[index]

    def __next__(self) -> Iterator[str]:
        index = 0
        yield self[index]
        index += 1

    def __str__(self) -> str:
        return self._raw_path

    def startswith(self, path: RouteTemplate) -> bool:
        return self._raw_path.startswith(str(path))

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RouteTemplate) and self._raw_path == other._raw_path

    def __len__(self) -> int:
        return len(self._raw_path)

    def __hash__(self) -> int:
        return hash(self._raw_path)

    def strip(self, other: RouteTemplate) -> RouteTemplate:
        """ Weird method, removes beginning of urlpath"""
        return RouteTemplate(self._raw_path.removeprefix(str(other)))

    def __add__(self, other: RouteTemplate) -> RouteTemplate:
        self_path = self._raw_path.removesuffix("/")
        other_path = other._raw_path.removeprefix("/")
        return RouteTemplate(self_path + "/" + other_path)

    def matches(self, request_path: str) -> bool:
        if self._raw_path == request_path \
            or (self._raw_path == "" and request_path == "/"):
            return True

        return False
