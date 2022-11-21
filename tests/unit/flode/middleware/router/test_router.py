from unittest import TestCase

from flode.di.container import Container
from flode.http_context_builder import HttpContextBuilder
from flode.http_method import HttpMethod
from flode.http_status import HttpStatus
from flode.middleware.endpoint.endpoint import Endpoint
from flode.middleware.endpoint.endpoint_result import EndpointResult
from flode.middleware.router.route import Route
from flode.middleware.router.route_pattern import RoutePattern
from flode.middleware.router.router import Router
from flode.middleware.router.router_options import RouterOptions


class TestRouter(TestCase):
    def test_get_routes_return_list_of_added_routes(self) -> None:
        class FirstController:
            @Route()
            def first_endpoint(self) -> EndpointResult: return EndpointResult("")

            @Route("/nested")
            def second_endpoint(self) -> EndpointResult: return EndpointResult("")

        class SecondController:
            @Route()
            def first_endpoint(self) -> EndpointResult: return EndpointResult("")

            @Route("/nested")
            def second_endpoint(self) -> EndpointResult: return EndpointResult("")

        opts = RouterOptions()
        opts.add_endpoint("/first", FirstController)
        opts.add_endpoint("/second", SecondController)
        router = Router(opts, Container())

        expected_routes = [RoutePattern("/first"), RoutePattern("/first/nested"), RoutePattern("/second"),
                           RoutePattern("/second/nested")]
        self.assertEqual(expected_routes, router.get_routes())

    def test_response_status_is_set_to_404_not_found_when_no_endpoint_could_be_found_for_path(self) -> None:
        router = Router(RouterOptions(), Container())
        context = HttpContextBuilder().path("/user/profile").build()
        router.handle_request(context)
        self.assertEqual(HttpStatus.NOT_FOUND, context.response.status)

    def test_endpoint_is_set_on_context_when_matching_request_path(self) -> None:
        class MyController:
            @Route()
            def my_method(self) -> EndpointResult: return EndpointResult("")

        container = Container()
        opts = RouterOptions()
        opts.add_endpoint("/test", MyController)
        router = Router(opts, container)
        context = HttpContextBuilder().path("/test").build()
        router.handle_request(context)
        controller = container.get_service(MyController)
        expected_endpoint = Endpoint(controller.my_method, Route("/test"))
        self.assertEqual(expected_endpoint, context.get_endpoint())

    def test_endpoints_can_specify_what_http_methods_they_support(self) -> None:
        class MyController:
            @Route(http_methods=[HttpMethod.GET])
            def get_method(self) -> EndpointResult:
                return EndpointResult("GET method")

            @Route(http_methods=[HttpMethod.POST])
            def post_method(self) -> EndpointResult:
                return EndpointResult("POST method")

        container = Container()
        opts = RouterOptions()
        opts.add_endpoint("/", MyController)
        router = Router(opts, container)
        controller = container.get_service(MyController)

        get_context = HttpContextBuilder().path("/").http_method(HttpMethod.GET).build()
        post_context = HttpContextBuilder().path("/").http_method(HttpMethod.POST).build()
        router.handle_request(get_context)
        router.handle_request(post_context)

        expected_get_endpoint = Endpoint(controller.get_method, Route())
        expected_post_endpoint = Endpoint(controller.post_method, Route(http_methods=[HttpMethod.POST]))
        self.assertEqual(expected_get_endpoint, get_context.get_endpoint())
        self.assertEqual(expected_post_endpoint, post_context.get_endpoint())

    def test_endpoints_can_support_multiple_http_methods(self) -> None:
        class MyController:
            @Route(http_methods=[HttpMethod.GET, HttpMethod.POST, HttpMethod.DELETE])
            def multi_method(self) -> EndpointResult:
                return EndpointResult("MULTI METHOD")

        container = Container()
        opts = RouterOptions()
        opts.add_endpoint("/", MyController)
        router = Router(opts, container)
        controller = container.get_service(MyController)

        get_context = HttpContextBuilder().path("/").http_method(HttpMethod.GET).build()
        post_context = HttpContextBuilder().path("/").http_method(HttpMethod.POST).build()
        delete_context = HttpContextBuilder().path("/").http_method(HttpMethod.DELETE).build()
        router.handle_request(get_context)
        router.handle_request(post_context)
        router.handle_request(delete_context)
        expected_endpoint = Endpoint(controller.multi_method, Route(http_methods=[HttpMethod.GET, HttpMethod.POST,
                                                                                  HttpMethod.DELETE]))
        self.assertEqual(expected_endpoint, get_context.get_endpoint())
        self.assertEqual(expected_endpoint, post_context.get_endpoint())
        self.assertEqual(expected_endpoint, delete_context.get_endpoint())
