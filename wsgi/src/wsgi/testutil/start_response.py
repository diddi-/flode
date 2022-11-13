from typing import List, Tuple

from wsgi.headers.http_header import HttpHeader
from wsgi.http_response import HttpResponse
from wsgi.http_status import HttpStatus


class StartResponse:
    """ This class simulate the WSGI start_response callable. It records the response status and headers in a
    HttpResponse object that can be extracted afterwards.

    https://peps.python.org/pep-3333/#the-start-response-callable
    """
    def __init__(self):
        self.http_response = HttpResponse()

    def __call__(self, status: str, headers: List[Tuple[str, str]]):
        status_code, status_message = status.split(" ")
        self.http_response.status = HttpStatus((int(status_code), status_message))

        http_headers: List[HttpHeader] = []
        for header in headers:
            http_headers.append(HttpHeader(header[0], header[1]))

        self.http_response.headers = http_headers
