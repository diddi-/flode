from typing import Type


class ServiceNotConfiguredException(Exception):
    def __init__(self, typ: Type[object]) -> None:
        super().__init__(f"No service has been configured for '{typ.__qualname__}'")
