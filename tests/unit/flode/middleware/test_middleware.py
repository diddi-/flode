from unittest import TestCase

from mockito import mock, verify

from flode.middleware.middleware import Middleware
from flode.middleware.no_options import NoOptions


class TestMiddleware(TestCase):
    def test_handle_request_calls_next_middleware(self) -> None:
        base_middleware = Middleware[NoOptions]()
        next_middleware = mock()
        http_context = mock()
        base_middleware.next_middleware = next_middleware

        base_middleware.handle_request(http_context)
        verify(next_middleware, times=1).handle_request(http_context)
