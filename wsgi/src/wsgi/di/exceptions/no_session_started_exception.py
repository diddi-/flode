class NoSessionStartedException(Exception):
    def __init__(self) -> None:
        super().__init__("No active container session has been started")
