from typing import TypeVar, Generic, Type, Callable, Dict, Any, Optional

from wsgi.di.provider import Provider

T = TypeVar("T")


class Using(Generic[T]):
    def __init__(self, typ: Type[T], callback: Callable[[Provider[T]], None]) -> None:
        self._type = typ
        self._callback = callback

    def using(self, cls: Type[T], kwargs: Optional[Dict[Any, Any]] = None) -> None:
        provider = Provider[T](self._type, cls, kwargs)
        self._callback(provider)
