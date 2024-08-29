from abc import ABC
from enum import Enum
from pathlib import Path
from typing import TypeAlias, Union

Str_or_Enum: TypeAlias = Union[str, Enum]
Int_or_Enum: TypeAlias = Union[int, Enum]
PathLike: TypeAlias = Union[str, Path]


### Custom unmutable and mutable Sequence only for tuple | list
# They which work with isinstance and issubclass checks, unlike type aliases like Union[list, tuple]
class TupleOrList(ABC):
    pass


TupleOrList.register(tuple)
TupleOrList.register(list)
