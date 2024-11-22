"""Utils"""

from collections.abc import Iterable, Mapping
from typing import Callable


def print_output(print_func: Callable = callable):
    """Prints the output of the decorated function with provided print function"""

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print_func(result)
            return result

        return wrapper

    return decorator


def print_argument_types(func):
    """Prints the types of in/output arguments of decorated function.

    A post-hoc handy/hacky tool to figure out argument types."""

    def get_collection_types(collection):
        """Helper to determine types of entries in a collection."""
        if isinstance(collection, Mapping):
            return {type(k): type(v) for k, v in collection.items()}
        elif isinstance(collection, Iterable) and not isinstance(
            collection, (str, bytes)
        ):
            return {type(item) for item in collection}
        return {type(collection)}

    def wrapper(*args, **kwargs):
        # Print input argument types
        print(f"\nCalling {func.__name__}...")
        for i, arg in enumerate(args):
            print(f"Arg {i}: {type(arg)}", end="")
            if isinstance(arg, (Iterable, Mapping)) and not isinstance(
                arg, (str, bytes)
            ):
                print(f" with entries of types: {get_collection_types(arg)}")
            else:
                print()

        for key, value in kwargs.items():
            print(f"Kwarg '{key}': {type(value)}", end="")
            if isinstance(value, (Iterable, Mapping)) and not isinstance(
                value, (str, bytes)
            ):
                print(f" with entries of types: {get_collection_types(value)}")
            else:
                print()

        # Call the original function
        result = func(*args, **kwargs)

        # Print output type
        print(f"Return: {type(result)}", end="")
        if isinstance(result, (Iterable, Mapping)) and not isinstance(
            result, (str, bytes)
        ):
            print(f" with entries of types: {get_collection_types(result)}")
        else:
            print()

        return result

    return wrapper
