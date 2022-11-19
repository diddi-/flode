from typing import Any, Dict, Generic, TypeVar, List, Optional, Type

from flode.di.exceptions.no_session_started_exception import NoSessionStartedException
from flode.di.provider.base_provider import BaseProvider
from flode.di.provider.lifetime import Lifetime

T = TypeVar("T")


class SessionProvider(Generic[T], BaseProvider[T]):
    """ The SingletonProvider will return the same instance each time requested. """
    _lifetime = Lifetime.SESSION

    def __init__(self, typ: Type[T], cls: Type[T]):
        super().__init__(typ, cls)
        self._instance: Optional[T] = None
        self._has_active_session: bool = False

    def start_session(self) -> None:
        self._has_active_session = True

    def stop_session(self) -> None:
        self._has_active_session = False
        self._instance = None

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        if not self._has_active_session:
            raise NoSessionStartedException()

        if self._instance is None:
            self._instance = self.provider(*args, **kwargs)

        return self._instance
