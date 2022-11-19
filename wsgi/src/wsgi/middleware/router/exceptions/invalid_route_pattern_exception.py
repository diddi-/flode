class InvalidRoutePatternException(Exception):
    """ Raised to indicate that the route pattern is not valid (e.g. contains invalid characters) """
    def __init__(self, pattern: str) -> None:
        super().__init__(f"'{pattern}' is not a valid route pattern")
