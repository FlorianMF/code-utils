from functools import wraps

__all__ = [
    'print_call',
]


def print_call(function):
    @wraps(function)
    def wrapper(*func_args, **func_kwargs):
        print('{} is called from the decorator' \
            'with arguments={} and kwargs={}'.format(
                function.__name__, func_args, func_kwargs))
        result = function(*func_args, **func_kwargs)
        print('{} returns {}'.format(function.__name__, result))
        return result
    return wrapper