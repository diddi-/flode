from typing import TypeVar, Generic, Type, Callable, Dict, Any, Optional

from wsgi.di.provider.default_provider import DefaultProvider
from wsgi.di.provider.singleton_provider import SingletonProvider
from wsgi.di.service_provider import ServiceProvider

T = TypeVar("T")


class Using(Generic[T]):
    def __init__(self, typ: Type[T], callback: Callable[[ServiceProvider[T]], None]) -> None:
        self._type = typ
        self._callback = callback

    def using(self, cls: Type[T], kwargs: Optional[Dict[Any, Any]] = None) -> None:
        provider = DefaultProvider[T](self._type, cls, kwargs)
        self._callback(provider)

    def using_singleton(self, cls: Type[T], kwargs: Optional[Dict[Any, Any]] = None) -> None:
        provider = SingletonProvider[T](self._type, cls, kwargs)
        self._callback(provider)
