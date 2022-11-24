from __future__ import annotations
from typing import Callable, TypeVar, ParamSpec

from flode.middleware.router.route import Route

P = ParamSpec("P")
R = TypeVar("R")


class Endpoint:
    def __init__(self, fn: Callable[P, R], route: Route):
        self.fn = fn
        self.route = route

    def __eq__(self, other: Endpoint) -> bool:
        return isinstance(other, Endpoint) and other.fn == self.fn and other.route == self.route
