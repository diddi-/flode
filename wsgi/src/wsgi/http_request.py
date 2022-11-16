from wsgi.http_method import HttpMethod


class HttpRequest:
    def __init__(self, path: str, method: HttpMethod):
        self.path = path
        self.http_method = method
