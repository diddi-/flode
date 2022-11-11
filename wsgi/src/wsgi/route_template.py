from __future__ import annotations
from typing import Any


class RouteTemplate:
    def __init__(self, path: str):
        self._raw_path = path

    def __getitem__(self, index: int) -> str:
        if self._raw_path.startswith("/"):
            index += 1  # split would cause first result to be empty

        return self._raw_path.split("/")[index]

    def __next__(self):
        index = 0
        yield self[index]
        index += 1

    def __str__(self) -> str:
        return self._raw_path

    def startswith(self, path: RouteTemplate) -> bool:
        return self._raw_path.startswith(path._raw_path)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, RouteTemplate) and self._raw_path == other._raw_path

    def __len__(self) -> int:
        return len(self._raw_path)

    def __hash__(self) -> hash:
        return hash(self._raw_path)

    def strip(self, other: RouteTemplate) -> RouteTemplate:
        """ Weird method, removes beginning of urlpath"""
        return RouteTemplate(self._raw_path.removeprefix(other._raw_path))

    def __add__(self, other: RouteTemplate) -> RouteTemplate:
        self_path = self._raw_path.removesuffix("/")
        other_path = other._raw_path.removeprefix("/")
        return RouteTemplate(self_path + "/" + other_path)
