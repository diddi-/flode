from http import HTTPStatus
from unittest import TestCase

from wsgi.app_builder import AppBuilder
from wsgi.controller.controller import Controller
from wsgi.controller.controller_result import ControllerResult
from wsgi.middleware.router.route import Route
from wsgi.middleware.router.router import Router, RouterOptions
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
        self.assertEqual(HTTPStatus.OK, response.status.code)
        self.assertEqual("It works!", response.body)
