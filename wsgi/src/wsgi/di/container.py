from inspect import signature
from typing import TypeVar, Dict, Type, cast, Any, Callable, ParamSpec, Optional

from wsgi.di.exceptions.missing_dependency_exception import MissingDependencyException
from wsgi.di.exceptions.service_not_configured_exception import ServiceNotConfiguredException
from wsgi.di.provider.base_provider import BaseProvider
from wsgi.di.provider.instance_provider import InstanceProvider
from wsgi.di.provider.lifetime import Lifetime
from wsgi.di.provider.singleton_provider import SingletonProvider
from wsgi.di.provider.transient_provider import TransientProvider
from wsgi.di.type_check import TypeCheck

T = TypeVar("T")
P = ParamSpec("P")
R = TypeVar("R")


class Container:
    def __init__(self) -> None:
        self._providers: Dict[Any, BaseProvider[Any]] = {
            Container: InstanceProvider[Container](Container, Container, self)}

    def register(self, provided_type: Type[T], provider: Optional[Type[T]] = None, lifetime: Lifetime = Lifetime.NONE,
                 type_check: TypeCheck = TypeCheck.STRICT) -> None:
        # If provider is not set, it is assumed to be same as the provided_type itself
        provider = provider if provider else provided_type

        if type_check.is_strict() and provided_type not in provider.mro():
            raise ValueError(f"'{provider.__qualname__}' can't be registered as the"
                             f" implementing class for '{provided_type.__qualname__}' in strict mode")

        if lifetime.is_singleton():
            self._providers[provided_type] = SingletonProvider[T](provided_type, provider)
        else:
            self._providers[provided_type] = TransientProvider[T](provided_type, provider)

    def register_instance(self, provided_type: Type[T], instance: T) -> None:
        self._providers[provided_type] = InstanceProvider[T](provided_type, type(instance), instance)

    def has_service(self, typ: Type[T]) -> bool:
        return typ in self._providers

    def get_service(self, typ: Type[T]) -> T:
        if typ not in self._providers:
            raise ServiceNotConfiguredException(typ)

        provider = self._providers[typ]
        args = []
        kwargs = {}
        for param in provider.get_parameters():
            if param.annotation in self._providers:
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                    args.append(self.get_service(param.annotation))
                else:
                    kwargs[param.name] = self.get_service(param.annotation)
            else:
                if param.name not in provider.custom_kwargs.keys():
                    raise MissingDependencyException(typ.__qualname__, param)
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
            # Filter *args and **kwargs.
            if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
                continue

            if param.annotation in self._providers:
                instance = self.get_service(param.annotation)
                if param.kind in (param.POSITIONAL_OR_KEYWORD, param.POSITIONAL_ONLY):
                    args.append(instance)
                else:
                    kwargs[param.name] = instance
            else:
                raise MissingDependencyException(fn.__qualname__, param)
        return fn(*args, **kwargs)
