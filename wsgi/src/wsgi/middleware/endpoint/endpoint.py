from typing import Type

from wsgi.controller.controller import Controller


class Endpoint:
    def __init__(self, controller: Type[Controller], method_name: str):
        self.controller = controller
        self.method_name = method_name
