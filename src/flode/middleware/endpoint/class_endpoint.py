from typing import Type

from flode.middleware.router.route import Route


class ClassEndpoint:
    def __init__(self, cls: Type[object], method_name: str, route: Route):
        self.controller = cls
        self.method_name = method_name
        self.route = route
