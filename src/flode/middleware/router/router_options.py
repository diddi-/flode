from typing import Dict, Type


class RouterOptions:
    def __init__(self) -> None:
        self.endpoints: Dict[str, Type[object]] = {}

    def add_endpoint(self, base_path: str, controller: Type[object]) -> None:
        self.endpoints[base_path] = controller
