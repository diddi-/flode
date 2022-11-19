from unittest import TestCase

from wsgi.app_builder import AppBuilder
from wsgi.http_status import HttpStatus
from wsgi.middleware.endpoint.endpoint_result import EndpointResult
from wsgi.middleware.router.route import Route
from wsgi.testutil.wsgi_test_client import WsgiTestClient


class TestWsgiApp(TestCase):
    def test_add_middleware_with_context_manager(self) -> None:
        class StatusController:
            @Route()
            def default_status(self) -> EndpointResult:
                return EndpointResult("It works!")

        builder = AppBuilder()
        with builder.add_routing() as opts:
            opts.add_endpoint("/status", StatusController)

        client = WsgiTestClient(builder.build())
        response = client.get("/status")
        self.assertEqual(HttpStatus.OK, response.status)
        self.assertEqual("It works!", response.body)

    def test_controller_with_nested_paths(self) -> None:
        class StatusController:
            @Route()
            def default_status(self) -> EndpointResult:
                return EndpointResult("default")

            @Route("/nested")
            def nested_status(self) -> EndpointResult:
                return EndpointResult("nested")

        builder = AppBuilder()
        with builder.add_routing() as opts:
            opts.add_endpoint("/status", StatusController)

        client = WsgiTestClient(builder.build())
        response = client.get("/status")
        self.assertEqual(HttpStatus.OK, response.status)
        self.assertEqual("default", response.body)

        response = client.get("/status/nested")
        self.assertEqual(HttpStatus.OK, response.status)
        self.assertEqual("nested", response.body)

    def test_endpoint_can_have_dependencies_injected(self) -> None:
        class MyService:
            message = "Up and running!"

        class StatusController:
            @Route()
            def default_status(self, service: MyService) -> EndpointResult:
                return EndpointResult(service.message)

        builder = AppBuilder()
        with builder.add_routing() as opts:
            opts.add_endpoint("/status", StatusController)

        builder.container.register(MyService)
        app = builder.build()

        client = WsgiTestClient(app)
        response = client.get("/status")
        self.assertEqual(MyService.message, response.body)
