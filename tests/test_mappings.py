from py_utils.mappings import (
    flatten_mapping,
    flatten_mapping_to_top_level,
    stringify_nested_mapping,
)

dict_ = {
    "top": {
        "intermediate1": {
            "low": 1,
        },
        "intermediate2": {
            "low": 2,
            "low3": 3,
        },
    },
}


def test_flatten_mapping():
    assert flatten_mapping(dict_, sep=".") == {
        "top.intermediate1.low": 1,
        "top.intermediate2.low": 2,
        "top.intermediate2.low3": 3,
    }


def test_flatten_mapping_separator():
    assert flatten_mapping(dict_, sep="/") == {
        "top/intermediate1/low": 1,
        "top/intermediate2/low": 2,
        "top/intermediate2/low3": 3,
    }


def test_mapping_to_top_level():
    assert flatten_mapping_to_top_level(dict_) == {"low": 2, "low3": 3}


def test_stringify_nested_mapping():
    res = {
        "top": {
            "intermediate1": {
                "low": "1",
            },
            "intermediate2": {
                "low": "2",
                "low3": "3",
            },
        },
    }
    assert stringify_nested_mapping(dict_) == res
