from wsgi.http_request import HttpRequest


class Controller:
    def __init__(self, request: HttpRequest):
        self.request = request
