from inspect import signature
from typing import TypeVar, Dict, Type, cast, Any, Callable, ParamSpec, List

from wsgi.di.service_provider import ServiceProvider
from wsgi.di.using import Using

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


class Container:
    # Ideally we don't want to use class variables. But at the moment our DI system will always create new instances
    # so this is a way to keep state between multiple instances of a Container. It's *bad*, yes, but one thing at the
    # time.
    _providers: Dict[Any, ServiceProvider[Any]] = {}
    def __init__(self) -> None:
        self.add_service(Container).using(Container)

    def _provider_callback(self, provider: ServiceProvider[Any]) -> None:
        self._providers[provider.provides_type] = provider

    def add_service(self, typ: Type[T]) -> Using[T]:
        return Using[T](typ, self._provider_callback)

    def get_instance(self, typ: Type[T]) -> T:
        provider = self._providers[typ]
        args = []
        kwargs = {}
        for param in provider.get_parameters():
            if param.annotation in self._providers:
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                    args.append(self.get_instance(param.annotation))
                else:
                    kwargs[param.name] = self.get_instance(param.annotation)

        for k, v in provider.custom_kwargs.items():
            kwargs[k] = v
        return cast(T, provider.instantiate(args, kwargs))

    def invoke(self, fn: Callable[P, R]) -> R:
        # We make a slight distinction between getting an instance (effectively invoking the constructor) and invoking
        # arbitrary callables. This is to support instantiation of singletons, which are handled by the
        # SingletonProvider.
        sig = signature(fn)
        args = []
        kwargs = {}
        for param in sig.parameters.values():
            if param.annotation in self._providers:
                instance = self.get_instance(param.annotation)
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                    args.append(instance)
                else:
                    kwargs[param.name] = instance

        return fn(*args, **kwargs)
