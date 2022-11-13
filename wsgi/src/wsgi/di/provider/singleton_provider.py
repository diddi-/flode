from typing import Any, Dict, Generic, TypeVar, List, Optional

from wsgi.di.provider.service_provider import ServiceProvider

T = TypeVar("T")


class SingletonProvider(Generic[T], ServiceProvider[T]):
    """ The SingletonProvider will return the same instance each time requested. """
    _instance: Optional[T] = None

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        if self._instance is None:
            self._instance = self.provider(*args, **kwargs)

        return self._instance
