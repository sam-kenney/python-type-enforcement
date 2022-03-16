"""Test enforce typing module on stdlib type hints."""  # pylint: disable=R0801
import pytest

from ..enforce_typing import enforce_typing
from ..exceptions import EnforcedTypingError


def test_enforce_typing_dict():
    """Test the enforce_typing decorator with a std dict."""

    @enforce_typing
    def test_list(arg_a: dict) -> str:
        return list(arg_a.values())[0]

    assert test_list({"index": "1"}) == "1"

    with pytest.raises(EnforcedTypingError):
        test_list({"index": 1})
    with pytest.raises(EnforcedTypingError):
        test_list((1, "1"))


def test_enforce_typing_list():
    """Test the enforce_typing decorator with a std list."""

    @enforce_typing
    def test_list(arg_a: list) -> str:
        return arg_a[0]

    assert test_list(["1", 1]) == "1"

    with pytest.raises(EnforcedTypingError):
        test_list([1, "1"])
    with pytest.raises(EnforcedTypingError):
        test_list((1, "1"))


def test_enforce_typing_tuple():
    """Test the enforce_typing decorator with a std tuple."""

    @enforce_typing
    def test_list(arg_a: tuple) -> str:
        return arg_a[0]

    assert test_list(("1", 1)) == "1"

    with pytest.raises(EnforcedTypingError):
        test_list((1, 1))
    with pytest.raises(EnforcedTypingError):
        test_list([1, 1])
