from typing import Any, Dict

from wsgi.http_response import HttpResponse
from wsgi.testutil.start_response import StartResponse
from wsgi.wsgiapp import WsgiApplication


class WsgiTestClient:
    def __init__(self, app: WsgiApplication) -> None:
        self.app = app

    def get(self, path: str) -> HttpResponse:
        environ = self._get_wsgi_environ()
        environ["PATH_INFO"] = path
        environ["REQUEST_METHOD"] = "GET"
        start_response = StartResponse()

        content = ""
        for content_byte in self.app(environ, start_response):
            content += content_byte.decode("utf-8")

        response = start_response.http_response
        response.body = content
        return response

    def _get_wsgi_environ(self) -> Dict[str, Any]:
        return {

        }
