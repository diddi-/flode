from inspect import Parameter, signature
from typing import Generic, TypeVar, Any, Dict, List, Type, Optional

from wsgi.di.provider.lifetime import Lifetime

T = TypeVar("T")


class BaseProvider(Generic[T]):
    _lifetime: Lifetime = Lifetime.NONE  # Will be overridden by subclasses

    def __init__(self, typ: Type[T], cls: Type[T], kwargs: Optional[Dict[str, Any]] = None) -> None:
        self._type = typ
        self._cls = cls
        self._custom_kwargs: Dict[str, Any] = kwargs if kwargs else {}

    @property
    def provides_type(self) -> Type[T]:
        return self._type

    @property
    def provider(self) -> Type[T]:
        return self._cls

    @property
    def custom_kwargs(self) -> Dict[str, Any]:
        return self._custom_kwargs

    @property
    def lifetime(self) -> Lifetime:
        return self._lifetime

    def has_custom_kwargs(self) -> bool:
        return len(self._custom_kwargs) > 0

    def get_parameters(self) -> List[Parameter]:
        sig = signature(self._cls.__init__)
        params: List[Parameter] = []

        for param in sig.parameters.values():
            # For the time being we skip *args and **kwargs. May have to change.
            if param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                params.append(param)

        params.pop(0)  # Remove 'self' parameter as it should not be passed to the constructor
        return params

    # Only SessionProvider care about sessions, this is a good indication that inheritance was not the best choice here.
    def start_session(self) -> None:
        pass

    def stop_session(self) -> None:
        pass

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        """ This will instantiate the service. Do not call this directly, it is only intended to be used
        by the DI container. """
        raise NotImplementedError()
