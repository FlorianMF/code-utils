from contextlib import contextmanager

__all__ = [
    'ignore_exception',
]

# def ignore_exceptions(function):
#     """
#     Decorator for supressing all exceptions
#     """
#     def wrapper(*func_args, **func_kwargs):
#         try:
#             return function(*func_args, **func_kwargs)
#         except:
#             pass
#     return wrapper

@contextmanager
def ignore_exceptions(*exceptions):
    try:
        yield
    except exceptions:
        pass


if __name__ == "__main__":
    with ignore_exceptions(ValueError):
        int('string')