import functools
import importlib
from time import time
from typing import List


def ttl_hash(seconds: int = 3600) -> int:
    """This function is use for Time-to-live hash by seconds

    :param seconds: Time to live in second(s), defaults to 3600
    :type seconds: int, optional
    :return: Hashed value
    :rtype: int
    """
    return round(time() / seconds)


def remove_duplicates(items: List[str], case_sensitive: bool = False) -> List[str]:
    """
    Remove duplicate strings from a list while preserving order.

    :param items: List of strings from which duplicates need to be removed.
    :param case_sensitive: Boolean flag indicating if the comparison should
                           be case sensitive. Defaults to False.
    :return: A list of strings with duplicates removed, order preserved.
    """
    d = dict()
    for item in items:
        k = str(item)
        if not case_sensitive:
            k = k.lower()
        if k in d:
            continue
        d[k] = item
    return list(d.values())


def import_class_by_path(class_path: str):
    """
    Import class by path
    :param class_path: module path of class
    :return: Class

    :example:
        import_class_by_path('core.db.DatabaseClass')
    """
    class_path = class_path.split('.')
    class_name = class_path.pop()
    module_path = '.'.join(class_path)
    module = importlib.import_module(module_path)
    c = getattr(module, class_name)
    return c


def method_dispatch(func):
    """Support single dispatch of a class's method
    """
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper
