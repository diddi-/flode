from flode.headers.http_header_collection import HttpHeaderCollection
from flode.http_status import HttpStatus


class HttpResponse:
    def __init__(self) -> None:
        self.status: HttpStatus = HttpStatus.OK
        self.body: str = ""
        self.headers = HttpHeaderCollection()
