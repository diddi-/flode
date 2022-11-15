from typing import Any, Dict, Generic, TypeVar, List, Type

from wsgi.di.provider.base_provider import BaseProvider
from wsgi.di.provider.lifetime import Lifetime

T = TypeVar("T")


class InstanceProvider(Generic[T], BaseProvider[T]):
    """ The InstanceProvider will return the same instance each time requested. """

    _lifetime = Lifetime.SINGLETON

    def __init__(self, typ: Type[T], cls: Type[T], instance: T) -> None:
        super().__init__(typ, cls)
        self._instance = instance

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        return self._instance
