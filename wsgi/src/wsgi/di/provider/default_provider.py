from typing import TypeVar, Dict, Any, Generic, List

from wsgi.di.service_provider import ServiceProvider

T = TypeVar("T")


class DefaultProvider(Generic[T], ServiceProvider[T]):
    """ !!BAD NAME!! This class should be named something to indicate how it actually works.

    The DefaultProvider will create a new instance each time it is requested to be instantiated.
    """

    def instantiate(self, args: List[Any], kwargs: Dict[str, Any]) -> T:
        """ This will instantiate the service. Do not call this directly, it is only intended to be used
        by the DI container. """
        return self.provider(*args, **kwargs)
