from abc import ABC, abstractmethod
from inspect import signature, Parameter
from typing import Generic, TypeVar, Type, Dict, Any, Optional, List, Tuple

T = TypeVar("T")


class ServiceProvider(Generic[T], ABC):
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

    def has_custom_kwargs(self) -> bool:
        return len(self._custom_kwargs) > 0

    def get_parameters(self) -> List[Parameter]:
        params: List[Parameter] = []
        sig = signature(self._cls.__init__)
        for param_name, param in sig.parameters.items():
            params.append(param)

        return params

    @abstractmethod
    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        """ This will instantiate the service. Do not call this directly, it is only intended to be used
        by the DI container. """
        raise NotImplementedError()
