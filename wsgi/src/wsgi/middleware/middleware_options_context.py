from types import TracebackType
from typing import Generic, TypeVar, Optional, Type

T = TypeVar("T")

class MiddlewareOptionsContext(Generic[T]):
    def __init__(self, opts: T):
        self.opts = opts

    def __enter__(self) -> T:
        return self.opts

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        pass
