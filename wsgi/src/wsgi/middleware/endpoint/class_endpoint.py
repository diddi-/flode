from typing import Type

class ClassEndpoint:
    def __init__(self, cls: Type[object], method_name: str):
        self.controller = cls
        self.method_name = method_name
