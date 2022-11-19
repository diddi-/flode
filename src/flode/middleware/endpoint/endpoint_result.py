from flode.http_status import HttpStatus


class EndpointResult:
    def __init__(self, content: str, status: HttpStatus = HttpStatus.OK):
        self.content = content
        self.status = status
