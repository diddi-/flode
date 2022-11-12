from typing import Generic, TypeVar, Type, Dict, Any, Optional

T = TypeVar("T")


class Provider(Generic[T]):
    def __init__(self, typ: Type[T], cls: Type[T], kwargs: Optional[Dict[str, Any]] = None) -> None:
        self._type = typ
        self._cls = cls
        self._custom_kwargs: Dict[str, Any] = kwargs if kwargs else {}

    @property
    def provides_for(self) -> Type[T]:
        return self._type

    @property
    def provider(self) -> Type[T]:
        return self._cls

    @property
    def custom_kwargs(self) -> Dict[str, Any]:
        return self._custom_kwargs

    def has_custom_kwargs(self) -> bool:
        return len(self._custom_kwargs) > 0
