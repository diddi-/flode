from wsgi.headers.http_header import HttpHeader


class ContentType(HttpHeader):
    def __init__(self, value: str) -> None:
        super().__init__("Content-Type", value)
