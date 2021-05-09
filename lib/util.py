from typing import Any, Type, Dict


def camel_to_snake_case(string: str) -> str:
    """Converts string content format from camelCase to snake_case

    >>> camel_to_snake_case('FooBar')
    'foo_bar'
    >>> camel_to_snake_case('fooBar')
    'foo_bar'
    """
    return "".join(
        ["_" + char.lower() if char.isupper() else char for char in string]
    ).lstrip("_")


class StrictDict(dict):
    """Blocks creation of new keys

    >>> d = StrictDict(foo='bar')
    >>> d['foo'] = 'buz'
    >>> d['bar'] = 'buz'
    Traceback (most recent call last):
    ...
    KeyError: 'bar is not a legal key of this StricDict'
    """

    def __setitem__(self, key, value):
        if key not in self:
            raise KeyError(f"{key} is not a legal key of this StricDict")
        super().__setitem__(key, value)


class Singleton(type):
    """Singleton metaclass

    >>> class Foo(metaclass=Singleton): pass
    >>> a = Foo()
    >>> b = Foo()
    >>> id(a) == id(b)
    True
    """

    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
