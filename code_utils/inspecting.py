import inspect
from collections.abc import Callable
from typing import Any


def filter_kwargs_to_expected(
    kwargs: dict[str, Any],
    func: Callable,
) -> dict[str, Any]:
    """Filter kwargs to the arguments a function accepts.

    If the function accepts any arguments via `**kwargs` the original dict is returned.

    The function accepting or not an arbitrary number of positional arguments via `*args`
    has no special effect on this function.

    Args:
        kwargs (Dict[str, Any]): kwargs to be filtered
        func (Callable): function on which signature to filter kwargs

    Returns:
        Dict[str, Any]: filtered version of `kwargs` reduced to what `func` accepts
    """
    args_spec = inspect.getfullargspec(func)
    # return input if function accepts any argument via kwargs
    if args_spec.varkw:
        return kwargs

    # Filter according to accepted args
    args_names = inspect.signature(func).parameters.keys()
    return {k: v for k, v in kwargs.items() if k in args_names}
