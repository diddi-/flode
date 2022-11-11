from typing import List, Tuple

from wsgi.headers.http_header import HttpHeader


class HttpHeaderCollection:
    def __init__(self):
        self._headers: List[HttpHeader] = []

    def add(self, header: HttpHeader) -> None:
        self._headers.append(header)

    def as_wsgi(self) -> List[Tuple[str, str]]:
        result: List[Tuple[str, str]] = []
        for header in self._headers:
            result.append((header.name, header.value))
        return result
