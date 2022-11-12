from enum import Enum, auto


class Lifetime(Enum):
    """ Lifetime of a service within the DI Container.
            * NONE - Services are instantiated on request and a new instance is returned each time.
            * SESSION - The same instance is returned each time until the container session is destroyed. (WIP)
            * SINGLETON - Same instance is always returned for the lifetime of the container.
    """
    NONE = auto()
    SESSION = auto()
    SINGLETON = auto()

    def is_none(self) -> bool:
        return self == Lifetime.NONE

    def is_session(self) -> bool:
        return self == Lifetime.SESSION

    def is_singleton(self) -> bool:
        return self == Lifetime.SINGLETON
