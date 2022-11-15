from unittest import TestCase

from wsgi.di.container import Container
from wsgi.endpoint.controller import Controller
from wsgi.endpoint.endpoint_result import EndpointResult
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
            def first_endpoint(self) -> EndpointResult: return EndpointResult("")

            @Route("/nested")
            def second_endpoint(self) -> EndpointResult: return EndpointResult("")

        class SecondController(Controller):
            @Route()
            def first_endpoint(self) -> EndpointResult: return EndpointResult("")

            @Route("/nested")
            def second_endpoint(self) -> EndpointResult: return EndpointResult("")

        opts = RouterOptions()
        opts.add_endpoint("/first", FirstController)
        opts.add_endpoint("/second", SecondController)
        router = Router(opts, Container())

        expected_routes = [RouteTemplate("/first"), RouteTemplate("/first/nested"), RouteTemplate("/second"),
                           RouteTemplate("/second/nested")]
        self.assertEqual(expected_routes, router.get_routes())

    def test_response_status_is_set_to_404_not_found_when_no_endpoint_could_be_found_for_path(self) -> None:
        router = Router(RouterOptions(), Container())
        context = HttpContext(HttpRequest(RouteTemplate("/test"), HttpMethod.GET))
        router.handle_request(context)
        self.assertEqual(HttpStatus.NOT_FOUND, context.response.status)

    def test_endpoint_is_set_on_context_when_matching_request_path(self) -> None:
        class MyController(Controller):
            @Route()
            def my_method(self) -> EndpointResult: return EndpointResult("")

        container = Container()
        opts = RouterOptions()
        opts.add_endpoint("/test", MyController)
        router = Router(opts, container)
        context = HttpContext(HttpRequest(RouteTemplate("/test"), HttpMethod.GET))
        router.handle_request(context)
        controller = container.get_service(MyController)
        self.assertEqual(controller.my_method, context.get_endpoint())
