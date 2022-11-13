from typing import Generic, TypeVar

T = TypeVar("T")

class MiddlewareOptionsContext(Generic[T]):
    def __init__(self, opts: T):
        self.opts = opts

    def __enter__(self) -> T:
        return self.opts

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
