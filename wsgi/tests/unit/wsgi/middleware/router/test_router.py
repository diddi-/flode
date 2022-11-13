from unittest import TestCase

from wsgi.controller.controller import Controller
from wsgi.controller.controller_result import ControllerResult
from wsgi.http_context import HttpContext
from wsgi.http_method import HttpMethod
from wsgi.http_request import HttpRequest
from wsgi.http_status import HttpStatus
from wsgi.middleware.router.route import Route
from wsgi.middleware.router.router import Router
from wsgi.middleware.router.router_options import RouterOptions
from wsgi.route_template import RouteTemplate


class TestRouter(TestCase):
    def test_get_routes_return_list_of_added_routes(self) -> None:
        class FirstController(Controller):
            @Route()
            def first_endpoint(self) -> ControllerResult: pass

            @Route("/nested")
            def second_endpoint(self) -> ControllerResult: pass

        class SecondController(Controller):
            @Route()
            def first_endpoint(self) -> ControllerResult: pass

            @Route("/nested")
            def second_endpoint(self) -> ControllerResult: pass

        opts = RouterOptions()
        opts.add_controller("/first", FirstController)
        opts.add_controller("/second", SecondController)
        router = Router(opts)

        expected_routes = [RouteTemplate("/first"), RouteTemplate("/first/nested"), RouteTemplate("/second"),
                           RouteTemplate("/second/nested")]
        self.assertEqual(expected_routes, router.get_routes())

    def test_response_status_is_set_to_404_not_found_when_no_endpoint_could_be_found_for_path(self) -> None:
        router = Router(RouterOptions())
        context = HttpContext(HttpRequest(RouteTemplate("/test"), HttpMethod.GET))
        router.handle_request(context)
        self.assertEqual(HttpStatus.NOT_FOUND, context.response.status)

    def test_endpoint_is_set_on_context_when_matching_request_path(self) -> None:
        class MyController(Controller):
            @Route()
            def my_method(self) -> ControllerResult: pass

        opts = RouterOptions()
        opts.add_controller("/test", MyController)
        router = Router(opts)
        context = HttpContext(HttpRequest(RouteTemplate("/test"), HttpMethod.GET))
        router.handle_request(context)
        self.assertEqual(MyController, context.get_endpoint().controller)
        self.assertEqual("my_method", context.get_endpoint().method_name)
