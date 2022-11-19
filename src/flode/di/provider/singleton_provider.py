from typing import Any, Dict, Generic, TypeVar, List, Optional, Type

from flode.di.provider.base_provider import BaseProvider
from flode.di.provider.lifetime import Lifetime

T = TypeVar("T")


class SingletonProvider(Generic[T], BaseProvider[T]):
    """ The SingletonProvider will return the same instance each time requested. """
    _lifetime = Lifetime.SINGLETON

    def __init__(self, typ: Type[T], cls: Type[T]):
        super().__init__(typ, cls)
        self._instance: Optional[T] = None

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        if self._instance is None:
            self._instance = self.provider(*args, **kwargs)

        return self._instance
