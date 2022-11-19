from enum import Enum, auto


class TypeCheck(Enum):
    """ This type check exists ONLY because there are limitations in some IDEs and static type checking tools like MyPy.
        Whenever a TypeCheck is requested, setting it to STRICT indicates that the code should do a strict type check at
        runtime, whereas LOOSE should behave like normal Python (i.e. no type checking validation at runtime). """
    STRICT = auto()
    LOOSE = auto()

    def is_strict(self) -> bool:
        return self == TypeCheck.STRICT

    def is_loose(self) -> bool:
        return self == TypeCheck.LOOSE
