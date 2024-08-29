# timing.py
from functools import wraps
import time

__all__ = [
    'timer',
    'time_all_class_methods',
]

def timer(func):
    """Decorates the passed function with a timer.
    It prints the time the function's call took.

    Parameters
    ----------
    func : function
        Function which execution shall be timed.

    Returns
    -------
    function
        The function wrapper with a timer.
    """
    @wraps(func)  # maintain all the info about the function
    def with_timer(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print ('{} ran in {}'.format(func.__name__, end - start))
        return result
    return with_timer

def time_all_class_methods(Cls):
    """Decorates all the methods of the passed class
    with the timer decorator.

    Parameters
    ----------
    Cls : class
        The class which methods shall be wrapper.

    Returns
    -------
    class
        The wrapper class
    """
    class NewCls():
        def __init__(self, *args, **kwargs):
            self.oInstance = Cls(*args, **kwargs)
        def __getattribute__(self, s):
            """
            this is called whenever any attribute of a NewCls object is accessed.
            This function first tries to get the attribute off NewCls.
            If it fails, it tries to get the attribute from self.oInstance
            (an instance of the wrapper class).
            If it manages to get the attribute from self.oInstance, and
            the attribute is an instance method then `timer` is applied.
            """
            try:
                x = self.super().__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            if type(x) == type(self.__init__): # it is an instance method
                return timer(x) # this is equivalent of just decorating the method with time_this
            else:
                return x
    return NewCls