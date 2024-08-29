import inspect
from collections import UserDict
from collections.abc import Callable
from typing import Any, Union

__all__ = ["Registry"]


class Registry(UserDict):
    """A registry that provides a name -> object mapping.

    To create a registry (e.g. a backbone registry):

    .. code-block:: python

        BACKBONE_REGISTRY = Registry("BACKBONE")

    To register an object:

    Use as a decorator

    .. code-block:: python

        @BACKBONE_REGISTRY.register()
        class MyBackbone:
            ...


        # or with kwargs:


        @BACKBONE_REGISTRY.register(name="new_name", metadata1="value")
        class MyBackbone:
            ...

    Or as a function call

    .. code-block:: python

        BACKBONE_REGISTRY.register(MyBackbone)
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

    def get(self, key: str, with_metadata: bool = False) -> Callable:
        return self.__getitem__(key, with_metadata=with_metadata)

    def __getitem__(self, key: str, with_metadata: bool = False) -> Callable:
        match = super().__getitem__(key)
        if with_metadata:
            return match
        return match["fn"]

    def register(
        self,
        fn: Callable = None,
        name: Union[str, None] = None,
        override: bool = False,
        **metadata: Any,
    ):
        # used as a function call
        if fn is not None:
            self._register(
                name or fn.__name__,
                fn,
                inspect.getfile(fn),
                override=override,
                metadata=metadata,
            )
            return fn

        # used as a decorator
        def deco(decorated_fn: Any) -> Any:
            self._register(
                name or decorated_fn.__name__,
                decorated_fn,
                inspect.getfile(decorated_fn),
                override=override,
                metadata=metadata,
            )
            return decorated_fn

        return deco

    def _register(
        self,
        key: str,
        fn: Callable,
        path: str,
        override: bool = False,
        metadata: Union[dict[str, Any], None] = None,
    ):
        if not callable(fn):
            raise ValueError(f"You can only register a callable, found: {fn}")

        if key in self.data and not override:
            # raise Error if callable is already registered and override=False
            raise ValueError(
                f"Function with name: {key} and metadata: {metadata} is already present within {self}."
                " HINT: Use `override=True`.",
            )
        else:
            self.data[key] = {
                "fn": fn,
                "path": path,
                "metadata": metadata or {},
            }

    def available_keys(self) -> list[str]:
        """Returns a list of registered callables."""
        return sorted(self.data.keys())

    def remove(self, key: str) -> None:
        """Removes the registered callable by name."""
        self.__delitem__(key)

    def __repr__(self) -> str:
        return f"{self.name}:\n\t{self.data}"

