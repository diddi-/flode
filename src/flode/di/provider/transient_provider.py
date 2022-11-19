from typing import Generic, TypeVar, Dict, Any, List

from flode.di.provider.base_provider import BaseProvider
from flode.di.provider.lifetime import Lifetime

T = TypeVar("T")


class TransientProvider(Generic[T], BaseProvider[T]):

    _lifetime = Lifetime.NONE

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        return self.provider(*args, **kwargs)
