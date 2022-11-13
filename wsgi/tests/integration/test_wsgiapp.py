from unittest import TestCase

from wsgi.app_builder import AppBuilder
from wsgi.controller.controller import Controller
from wsgi.controller.controller_result import ControllerResult
from wsgi.http_status import HttpStatus
from wsgi.middleware.router.route import Route
from wsgi.middleware.router.router import Router
from wsgi.middleware.router.router_options import RouterOptions
from wsgi.testutil.wsgi_test_client import WsgiTestClient


class TestWsgiApp(TestCase):
    def test_add_middleware_with_context_manager(self) -> None:
        class StatusController(Controller):
            @Route()
            def default_status(self) -> ControllerResult:
                return ControllerResult("It works!")

        builder = AppBuilder()
        with builder.add_middleware(Router, RouterOptions) as opts:
            opts.add_controller("/status", StatusController)

        client = WsgiTestClient(builder.build())
        response = client.get("/status")
        self.assertEqual(HttpStatus.OK, response.status)
        self.assertEqual("It works!", response.body)

    def test_controller_with_nested_paths(self) -> None:
        class StatusController(Controller):
            @Route()
            def default_status(self) -> ControllerResult:
                return ControllerResult("default")
            @Route("/nested")
            def nested_status(self) -> ControllerResult:
                return ControllerResult("nested")

        builder = AppBuilder()
        with builder.add_middleware(Router, RouterOptions) as opts:
            opts.add_controller("/status", StatusController)

        client = WsgiTestClient(builder.build())
        response = client.get("/status")
        self.assertEqual(HttpStatus.OK, response.status)
        self.assertEqual("default", response.body)

        response = client.get("/status/nested")
        self.assertEqual(HttpStatus.OK, response.status)
        self.assertEqual("nested", response.body)
