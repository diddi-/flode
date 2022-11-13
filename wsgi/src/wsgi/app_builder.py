from __future__ import annotations

from typing import Optional, Type, TypeVar, List

from wsgi.di.container import Container
from wsgi.di.provider.lifetime import Lifetime
from wsgi.middleware.endpoint.endpoint_middleware import EndpointMiddleware
from wsgi.middleware.middleware import Middleware
from wsgi.middleware.middleware_options_context import MiddlewareOptionsContext
from wsgi.wsgiapp import WsgiApplication

T = TypeVar("T")


class AppBuilder:
    def __init__(self):
        self._container = Container()
        self._middlewares: List[Type[Middleware]] = []

    def add_middleware(self, middleware: Type[Middleware[T]], _opts: Optional[Type[T]] = None) \
            -> MiddlewareOptionsContext[T]:
        # NOTE: The second argument '_opts: Type[T]' is *only* a workaround for the PyCharm IDE as it can't infer the
        # options type from a generic base class: https://youtrack.jetbrains.com/issue/PY-53082
        self._middlewares.append(middleware)
        self._container.add_service(middleware).using(middleware, Lifetime.SINGLETON)
        middleware_options = middleware.OPTS()
        self._container.add_service(type(middleware_options)).using_instance(middleware_options)
        return MiddlewareOptionsContext[T](middleware_options)

    def build(self) -> WsgiApplication:
        self.add_middleware(EndpointMiddleware)

        for index in range(0, len(self._middlewares) - 1):
            middleware = self._container.get_service(self._middlewares[index])
            middleware.next_middleware = self._container.get_service(self._middlewares[index + 1])

        return WsgiApplication(self._container.get_service(self._middlewares[0]))