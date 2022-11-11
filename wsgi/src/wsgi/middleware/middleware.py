from typing import Optional

from wsgi.http_context import HttpContext


class Middleware:
    """ Middleware base class. Subclasses that inherit from Middleware should implement the handle_request() method. """
    def __init__(self):
        self.next_middleware: Optional[Middleware] = None

    def handle_request(self, context: HttpContext) -> None:
        self.next(context)

    def next(self, context: HttpContext) -> None:
        if self.next_middleware:
            self.next_middleware.handle_request(context)
