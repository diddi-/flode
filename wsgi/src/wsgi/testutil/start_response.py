from typing import List, Tuple

from wsgi.headers.http_header import HttpHeader
from wsgi.headers.http_header_collection import HttpHeaderCollection
from wsgi.http_response import HttpResponse
from wsgi.http_status import HttpStatus


class StartResponse:
    """ This class simulate the WSGI start_response callable. It records the response status and headers in a
    HttpResponse object that can be extracted afterwards.

    https://peps.python.org/pep-3333/#the-start-response-callable
    """
    def __init__(self) -> None:
        self.http_response = HttpResponse()

    def __call__(self, status: str, headers: List[Tuple[str, str]]) -> None:
        parts = status.split(" ")
        if len(parts) < 2:
            raise ValueError("Status code must consist of a code followed by a reason (e.g. 200 'OK')")

        status_code = parts[0]
        status_reason = str.join(" ", parts[1:])
        self.http_response.status = HttpStatus((int(status_code), status_reason))

        http_headers = HttpHeaderCollection()
        for header in headers:
            http_headers.add(HttpHeader(header[0], header[1]))

        self.http_response.headers = http_headers
