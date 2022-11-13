from http import HTTPStatus
from unittest import TestCase

from wsgi.controller.controller import Controller
from wsgi.controller.controller_result import ControllerResult
from wsgi.middleware.router.route import Route
from wsgi.middleware.router.router import Router, RouterOptions
from wsgi.testutil.wsgi_test_client import WsgiTestClient
from wsgi.wsgiapp import WsgiApplication


class TestWsgiApp(TestCase):

    def test_single_controller_get_method(self) -> None:
        class StatusController(Controller):
            @Route()
            def default_status(self) -> ControllerResult:
                return ControllerResult("It works!")
        app = WsgiApplication()
        router = Router()
        router.add_controller("/status", StatusController)
        app.add_middleware(router)

        client = WsgiTestClient(app)
        response = client.get("/status")
        self.assertEqual(HTTPStatus.OK, response.status.code)
        self.assertEqual("It works!", response.body)

    def test_add_middleware_with_context_manager(self) -> None:
        class StatusController(Controller):
            @Route()
            def default_status(self) -> ControllerResult:
                return ControllerResult("It works!")
        app = WsgiApplication()
        with app.add_middleware_ctx(Router, RouterOptions) as opts:
            opts.add_controller("/status", StatusController)

        client = WsgiTestClient(app)
        response = client.get("/status")
        self.assertEqual(HTTPStatus.OK, response.status.code)
        self.assertEqual("It works!", response.body)
