from numbers import Number
import operator
from typing import Union

__all__ = [
    "round_to_nearest",
    "clip",
    "clamp",
    "threshold",
    "abs_threshold",
]


def round_to_nearest(
    x: Union[str, int, float],
    multiple: Union[str, int, float] = 1,
):
    """Rounding function which allows to set a different multiple than 1. If multiple is zero, the input is
    returned.

    Parameters
    ----------
    x: number
        number which shall be rounded

    multiple: number, optional
        Int to which shall be rounded. Defaults to 1.

    Returns
    -------
    float
        Value x rounded to the next integer 'multiple'
    """
    # transform `x` to number
    if isinstance(x, str):
        if x.isdigit():  # is integer
            x = int(x)
        else:
            x = float(x)

    # transform `multiple` to number
    if isinstance(multiple, str):
        if multiple.isdigit():  # is integer
            multiple = int(multiple)
        else:
            multiple = float(multiple)

    if multiple == 0:
        return x

    result = multiple * round(x / multiple)
    if isinstance(x, float):
        result = float(result)
    return result


def clip(a: Number, a_min: Number, a_max: Number) -> Number:
    """Clip a Number between a minimal and maximal value.

    Equivalent of np.clip or torch.clamp for float/integer.
    """
    return min(a_max, max(a, a_min))


clamp = clip


def threshold(
    value: Union[int, float],
    threshold: Union[int, float],
    mode: str = "lt",
) -> bool:
    criterions = {
        "lt": operator.lt,
        "le": operator.le,
        "ge": operator.ge,
        "gt": operator.gt,
    }
    assert mode in criterions
    return criterions[mode](value, threshold)


def abs_threshold(
    value: Union[int, float],
    thresh: Union[int, float],
    mode: str = "lt",
) -> bool:
    return threshold(abs(value), thresh, mode)
