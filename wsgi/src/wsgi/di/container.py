from inspect import signature
from typing import TypeVar, Dict, Type, cast, Any

from wsgi.di.provider import Provider
from wsgi.di.using import Using

T = TypeVar("T")


class Container:
    # Ideally we don't want to use class variables. But at the moment our DI system will always create new instances
    # so this is a way to keep state between multiple instances of a Container. It's *bad*, yes, but one thing at the
    # time.
    _providers: Dict[Any, Provider[Any]] = {}
    def __init__(self) -> None:
        self.resolve(Container).using(Container)

    def _provider_callback(self, provider: Provider[Any]) -> None:
        self._providers[provider.provides_for] = provider

    def resolve(self, typ: Type[T]) -> Using[T]:
        return Using[T](typ, self._provider_callback)

    def get_instance(self, typ: Type[T]) -> T:
        provider = self._providers[typ]
        sig = signature(provider.provider.__init__)
        args = []
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param.annotation in self._providers:
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                    args.append(self.get_instance(param.annotation))
                else:
                    kwargs[param_name] = self.get_instance(param.annotation)

        for k, v in provider.custom_kwargs.items():
            kwargs[k] = v
        return cast(T, provider.provider(*args, **kwargs))
