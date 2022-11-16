from wsgi.http_method import HttpMethod
from wsgi.route_template import RouteTemplate


class HttpRequest:
    def __init__(self, path: RouteTemplate, method: HttpMethod):
        self.path = path
        self.http_method = method
