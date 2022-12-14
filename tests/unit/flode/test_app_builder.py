from unittest import TestCase

from flode.app_builder import AppBuilder
from flode.middleware.endpoint.endpoint_middleware import EndpointMiddleware
from flode.middleware.middleware import Middleware
from flode.middleware.no_options import NoOptions


class TestAppBuilder(TestCase):
    def test_app_builder_adds_endpoint_middleware_to_the_end_of_the_middleware_chain(self) -> None:
        class MyMiddleware(Middleware[NoOptions]): pass
        builder = AppBuilder()
        builder.add_middleware(MyMiddleware)
        app = builder.build()

        self.assertIsInstance(app.container.get_service(MyMiddleware).next_middleware, EndpointMiddleware)

    def test_middlewares_can_be_configured_using_middleware_options_context(self) -> None:
        class MyOpts: pass
        class MyMiddleware(Middleware[MyOpts]):
            _OPTS = MyOpts

        builder = AppBuilder()
        with builder.add_middleware(MyMiddleware, MyOpts) as opts:
            self.assertIsInstance(opts, MyOpts)

        app = builder.build()
        self.assertTrue(app.container.has_service(MyMiddleware))
        self.assertTrue(app.container.has_service(MyOpts))

    def test_middlewares_are_added_as_singletons(self) -> None:
        class MyMiddleware(Middleware[NoOptions]): pass

        builder = AppBuilder()
        builder.add_middleware(MyMiddleware)
        app = builder.build()

        self.assertEqual(app.container.get_service(MyMiddleware), app.container.get_service(MyMiddleware))
