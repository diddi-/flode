from inspect import Parameter
from typing import Type


class MissingDependencyException(Exception):
    def __init__(self, name: str, param: Parameter) -> None:
        super().__init__(f"Parameter '{param}' could not be resolved for '{name}'")
