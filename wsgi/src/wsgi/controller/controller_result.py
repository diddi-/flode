from wsgi.http_status import HttpStatus


class ControllerResult:
    def __init__(self, content: str, status: HttpStatus = HttpStatus.OK):
        self.content = content
        self.status = status
