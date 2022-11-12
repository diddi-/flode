from typing import Any, Dict, Generic, TypeVar, List

from wsgi.di.service_provider import ServiceProvider

T = TypeVar("T")


class SingletonProvider(Generic[T], ServiceProvider[T]):
    """ The SingletonProvider will return the same instance each time requested. """
    _INSTANCE: T = None

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        if self._INSTANCE is None:
            self._INSTANCE = self.provider(*args, **kwargs)

        return self._INSTANCE
