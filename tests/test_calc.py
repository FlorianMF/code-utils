import pytest

from py_utils.calc import round_to_nearest


### round_to_nearest
class TestRoundNearest:
    @pytest.mark.parametrize(
        ("x", "multiple", "expected_type"),
        (
            (5, "1", int),
            ("5", 1, int),
            (5, "1", int),
            ("5", 1, int),
            ("5", "1", int),
            (5, "1.0", float),
            ("5.0", 1, float),
            ("5.0", "1.0", float),
        ),
    )
    def test_numeric_string(self, x, multiple, expected_type):
        """Check that the function works for string reps of int and float."""
        assert isinstance(round_to_nearest(x, multiple), expected_type)

    @pytest.mark.parametrize(
        ("x", "multiple"),
        (
            (5, "b"),
            ("a", 1),
            ("a", "b"),
        ),
    )
    def test_alphabetic_input(self, x, multiple):
        """Check that the function raises an error when the string input does not represent a number."""
        with pytest.raises(ValueError):
            round_to_nearest(x, multiple)

    @pytest.mark.parametrize(
        ("x", "multiple", "expected"),
        (
            (71, 1, 71),
            (71, 2, 72),
            (71, 3, 72),
            (71, 4, 72),
            (71, 5, 70),
            (71, 6, 72),
            (71, 7, 70),
            (71, 8, 72),
            (71, 9, 72),
            (71, 10, 70),
            (71, 11, 66),
            (71, 12, 72),
            (71, 13, 65),
            (71, 14, 70),
            (71, 15, 75),
        ),
    )
    def test_multiples(self, x, multiple, expected):
        """Test different values for the `multiple` argument."""
        assert round_to_nearest(x, multiple) == expected

    @pytest.mark.parametrize(
        ("x", "multiple", "expected"),
        (
            (1.111111, 0.1, 1.1),
            (1.111111, 0.01, 1.11),
            (1.111111, 0.001, 1.111),
            (1.111111, 0.0001, 1.1111),
            (1.111111, 0.00001, 1.11111),
            (1.111111, 0.000001, 1.111111),
        ),
    )
    def test_precisions(self, x, multiple, expected):
        """Check the rounding to different numbers of digits of precision."""
        assert round_to_nearest(x, multiple) == expected
