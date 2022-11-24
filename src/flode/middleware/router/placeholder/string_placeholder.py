from typing import Any


class StringPlaceholder:
    """ Represents a single placeholder inside a RoutePattern. """

    def __init__(self, name: str, location: int) -> None:
        self.name = name
        self.location = location

    def matches(self, _value: str) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, type(self)) and other.name == self.name and other.location == self.location

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self.name}>"
