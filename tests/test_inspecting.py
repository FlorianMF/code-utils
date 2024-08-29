from python_utils.inspecting import filter_kwargs_to_expected


def func_no_args_kwargs():
    pass


def func_args_only(a, b):
    pass


def func_kwargs_only(**kwargs):
    pass


def func_args_kwargs(a, b, **kwargs):
    pass


kwargs = {"a": 1, "b": 2, "c": 3}


def test_func_no_args_kwargs():
    assert filter_kwargs_to_expected(kwargs, func_no_args_kwargs) == {}


def test_func_args_only():
    assert filter_kwargs_to_expected(kwargs, func_args_only) == {
        "a": 1,
        "b": 2,
    }


def test_func_kwargs_only():
    assert filter_kwargs_to_expected(kwargs, func_kwargs_only) == kwargs


def test_func_args_kwargs():
    assert filter_kwargs_to_expected(kwargs, func_args_kwargs) == kwargs
