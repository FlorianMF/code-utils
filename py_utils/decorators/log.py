# timing.py
from functools import wraps, partial
import logging

__all__ = [
    'log',
]


def log(func=None, *, logger=logging.getLogger(__name__), level='info'):
    if func is None:
        """A partial is a "non-complete function call" that includes
        a function and some arguments, so that they are passed around
        as one object without actually calling the function yet.
        """
        return partial(log, logger=logger, level=level)
    @wraps(func)  # maintain all the info about the function
    def wrapper(*args, **kwargs):
        logger.log(level, '{} was called with args: {} and kwargs: {}'.format(func.__name__, args, kwargs))
        result = func(*args, **kwargs)
        logger.log(level, 'return value: {}'.format(func, result))
        return result
    return wrapper
