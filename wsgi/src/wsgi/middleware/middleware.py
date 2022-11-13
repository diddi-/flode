from typing import Optional, Generic, TypeVar, Type

from wsgi.http_context import HttpContext
from wsgi.middleware.no_config import NoConfig

OPTS_TYPE = TypeVar("OPTS_TYPE")


class Middleware(Generic[OPTS_TYPE]):
    """ Middleware base class. Subclasses that inherit from Middleware should implement the handle_request() method. """

    OPTS: Type[OPTS_TYPE] = NoConfig # Defines the middleware's class type for its options.

    def __init__(self) -> None:
        self.next_middleware: Optional[Middleware] = None

    def handle_request(self, context: HttpContext) -> None:
        self.next(context)

    def next(self, context: HttpContext) -> None:
        if self.next_middleware:
            self.next_middleware.handle_request(context)
