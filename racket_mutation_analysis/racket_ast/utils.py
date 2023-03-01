from typing import Container

from .scheme_reader import Identifier, SList


def is_call_to(slist: SList, func_name: str) -> bool:
    """
    Returns True if the given SList is a call to a function named
    `func_name`.
    """
    if len(slist.items) == 0:
        return False

    first = slist.items[0]
    return isinstance(first, Identifier) and first.name == func_name


def is_call_to_one_of(slist: SList, func_names: Container[str]) -> bool:
    """
    Returns True if the given SList is a call to one of the functions
    contained in `func_names`.
    """
    if len(slist.items) == 0:
        return False

    first = slist.items[0]
    return isinstance(first, Identifier) and first.name in func_names
