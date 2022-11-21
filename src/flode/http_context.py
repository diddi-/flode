from typing import Optional

from flode.http_request import HttpRequest
from flode.http_response import HttpResponse
from flode.middleware.endpoint.endpoint import Endpoint


class HttpContext:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.response = HttpResponse()

        self._endpoint: Optional[Endpoint] = None

    def set_endpoint(self, endpoint: Endpoint) -> None:
        self._endpoint = endpoint

    def get_endpoint(self) -> Endpoint:
        if not self._endpoint:
            raise ValueError("No endpoint set!")

        return self._endpoint
