from typing import Generic, TypeVar, Dict, Any, List

from wsgi.di.provider.base_provider import BaseProvider
from wsgi.di.provider.lifetime import Lifetime

T = TypeVar("T")


class TransientProvider(Generic[T], BaseProvider[T]):

    _lifetime = Lifetime.NONE

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        return self.provider(*args, **kwargs)
