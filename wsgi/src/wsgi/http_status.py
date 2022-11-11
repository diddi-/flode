from enum import Enum


class HttpStatus(Enum):
    OK = (200, "OK")
    BAD_REQUEST = (400, "BAD REQUEST")
    NOT_FOUND = (404, "NOT FOUND")
    INTERNAL_SERVER_ERROR = (500, "INTERNAL SERVER ERROR")

    def __str__(self) -> str:
        return self.value[1]

    def __int__(self) -> int:
        return self.value[0]

    @property
    def code(self) -> int:
        return int(self)

    @property
    def reason(self) -> str:
        return str(self)
