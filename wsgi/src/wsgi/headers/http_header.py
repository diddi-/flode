from typing import Iterable


class HttpHeader:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f"{self.name}: {self.value}"
