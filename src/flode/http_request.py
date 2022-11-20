from flode.http_method import HttpMethod
from flode.middleware.router.url_path import UrlPath


class HttpRequest:
    def __init__(self, path: UrlPath, method: HttpMethod):
        self.path = path
        self.http_method = method
