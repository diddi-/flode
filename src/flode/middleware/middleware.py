from typing import Optional, Generic, TypeVar, Type, cast

from flode.http_context import HttpContext
from flode.middleware.no_options import NoOptions

# Python 3.12 will allow us to specify a default type, e.g. default=NoOptions. However, in the meantime all subclasses
# will have to inherit from Middleware[NoOptions] if they do not need a specific options class.
# https://peps.python.org/pep-0696/
OPTS_TYPE = TypeVar("OPTS_TYPE")


class Middleware(Generic[OPTS_TYPE]):
    """ Middleware base class. Subclasses that inherit from Middleware should implement the handle_request() method. """

    _OPTS: Type[OPTS_TYPE] # Defines the middleware's class type for its options.

    def __init__(self) -> None:
        self.next_middleware: Optional[Middleware[OPTS_TYPE]] = None

    def handle_request(self, context: HttpContext) -> None:
        self.next(context)

    def next(self, context: HttpContext) -> None:
        if self.next_middleware:
            self.next_middleware.handle_request(context)

    @classmethod
    def get_options(cls) -> OPTS_TYPE:
        if hasattr(cls, "_OPTS"):
            return cast(OPTS_TYPE, cls._OPTS())

        return cast(OPTS_TYPE, NoOptions())
