from py_utils.types import TupleOrList

def test_TupleOrList():
    # class should not be inherited from
    # __subclasses__() returns the real subclasses
    assert TupleOrList.__subclasses__() == []

    assert isinstance(tuple(), TupleOrList)
    assert issubclass(tuple, TupleOrList)

    assert isinstance(list(), TupleOrList)
    assert issubclass(list, TupleOrList)
