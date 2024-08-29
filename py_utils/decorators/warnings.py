import warnings
from functools import wraps

__all__ = [
    'deprecated',
]

def deprecated(function):
    """
    This marks functions as deprecated.
    A warning is emitted when the function is used.
    """
    @wraps(function)
    def wrapper(*func_args, **func_kwargs):
        warnings.warn("Call to deprecated function %s." % function.__name__,
                      category=DeprecationWarning)
        return function(*func_args, **func_kwargs)
    return wrapper