from typing import Dict, Type

from wsgi.controller.controller import Controller


class RouterOptions:
    def __init__(self) -> None:
        self.endpoints: Dict[str, Type[Controller]] = {}

    def add_controller(self, base_path: str, controller: Type[Controller]) -> None:
        self.endpoints[base_path] = controller
