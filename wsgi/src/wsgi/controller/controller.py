from typing import Optional

from wsgi.http_request import HttpRequest


class Controller:
    def __init__(self) -> None:
        self.request = Optional[HttpRequest]
