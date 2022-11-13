from inspect import signature
from typing import TypeVar, Dict, Type, cast, Any, Callable, ParamSpec, Optional

from wsgi.di.exceptions.missing_dependency_exception import MissingDependencyException
from wsgi.di.exceptions.service_not_configured_exception import ServiceNotConfiguredException
from wsgi.di.provider.lifetime import Lifetime
from wsgi.di.provider.service_provider import ServiceProvider
from wsgi.di.provider.singleton_provider import SingletonProvider
from wsgi.di.type_check import TypeCheck
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
        self.add_service(Container).using_instance(self)

    def _provider_callback(self, provider: ServiceProvider[Any]) -> None:
        self._providers[provider.provides_type] = provider

    def add_service(self, typ: Type[T]) -> Using[T]:
        # The reason we're chaining with a Using here instead of just taking two arguments to add_service() is because
        # the typing system is not strict enough. With add_service(Type[T], Type[T]), the typing system will go up the
        # inheritance chain of both arguments to infer a common type, which may be 'object'. As such, any
        # two types can be passed and still be valid by the typing system. This is different for return values however,
        # so add_service(Type[T]) -> Using[T] will bind the two types to be exactly the same.
        return Using[T](typ, self._provider_callback)

    def register(self, service: Type[T], concrete: Optional[Type[T]] = None, lifetime: Lifetime = Lifetime.NONE,
                 type_check: TypeCheck = TypeCheck.STRICT) -> None:
        # If not concrete is set to anything, assume service is also the concrete type
        implementing_class = concrete if concrete else service

        if type_check.is_strict() and service not in implementing_class.mro():
            raise ValueError(f"'{implementing_class.__qualname__}' can't be registered as the"
                             f" implementing class for '{service.__qualname__}' in strict mode")

        if lifetime.is_singleton():
            provider = SingletonProvider[T](service, implementing_class)
        else:
            provider = ServiceProvider[T](service, implementing_class)

        self._providers[provider.provides_type] = provider

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
