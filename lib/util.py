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
