class StringPlaceholder:
    """ Represents a single placeholder inside a RoutePattern. """

    def __init__(self, name: str, location: int) -> None:
        self.name = name
        self.location = location

    def matches(self, _value: str) -> bool:
        return True
