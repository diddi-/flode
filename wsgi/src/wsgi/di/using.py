from typing import TypeVar, Generic, Type, Callable, Dict, Any, Optional

from wsgi.di.provider.instance_provider import InstanceProvider
from wsgi.di.provider.lifetime import Lifetime
from wsgi.di.provider.singleton_provider import SingletonProvider
from wsgi.di.provider.service_provider import ServiceProvider

T = TypeVar("T")


class Using(Generic[T]):
    def __init__(self, typ: Type[T], callback: Callable[[ServiceProvider[T]], None]) -> None:
        self._type = typ
        self._callback = callback

    def using(self, cls: Type[T], lifetime: Lifetime = Lifetime.NONE, kwargs: Optional[Dict[Any, Any]] = None) -> None:
        if lifetime.is_singleton():
            provider = SingletonProvider[T](self._type, cls, kwargs)
        else:
            provider = ServiceProvider[T](self._type, cls, kwargs)
        self._callback(provider)

    def using_instance(self, instance: T) -> None:
        """ Use an already instantiated instance of a service. The lifetime is always Singleton. """
        self._callback(InstanceProvider(self._type, type(instance), instance))
