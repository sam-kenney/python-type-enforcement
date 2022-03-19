"""Test enforce typing module on stdlib type hints."""
import pytest

from ..enforce_typing import enforce_typing
from ..exceptions import EnforcedTypingError


def test_enforce_typing_dict():
    """Test the enforce_typing decorator with a std dict."""

    @enforce_typing
    def test_dict(arg_a: dict) -> str:
        return list(arg_a.values())[0]

    assert test_dict({"index": "1"}) == "1"

    with pytest.raises(EnforcedTypingError):
        test_dict({"index": 1})
    with pytest.raises(EnforcedTypingError):
        test_dict((1, "1"))


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
    def test_tuple(arg_a: tuple) -> str:
        return arg_a[0]

    assert test_tuple(("1", 1)) == "1"

    with pytest.raises(EnforcedTypingError):
        test_tuple((1, 1))
    with pytest.raises(EnforcedTypingError):
        test_tuple([1, 1])


def test_enforce_typing_string():
    """Test the enforce_typing decorator with a std string."""

    @enforce_typing
    def test_str(arg_a: str) -> str:
        return arg_a

    assert test_str("1") == "1"

    with pytest.raises(EnforcedTypingError):
        test_str(1)
    with pytest.raises(EnforcedTypingError):
        test_str({"1": 1})
    with pytest.raises(EnforcedTypingError):
        test_str([1, 1])
    with pytest.raises(EnforcedTypingError):
        test_str((1, 1))


def test_enforce_typing_int():
    """Test the enforce_typing decorator with a std int."""

    @enforce_typing
    def test_int(arg_a: int) -> int:
        return arg_a

    assert test_int(1) == 1

    with pytest.raises(EnforcedTypingError):
        test_int("1")
    with pytest.raises(EnforcedTypingError):
        test_int({"1": 1})
    with pytest.raises(EnforcedTypingError):
        test_int([1, 1])
    with pytest.raises(EnforcedTypingError):
        test_int((1, 1))


def test_enforce_typing_return_type_int():
    """Test the return type is an int."""

    @enforce_typing
    def test_return_int(arg_a: int) -> int:
        return arg_a

    @enforce_typing
    def test_fail_return_int(arg_a: str) -> int:
        return arg_a

    assert test_return_int(1) == 1

    with pytest.raises(EnforcedTypingError):
        test_fail_return_int("1")


def test_enforce_typing_return_type_str():
    """Test the return type is an int."""

    @enforce_typing
    def test_return_str(arg_a: int) -> str:
        return str(arg_a)

    @enforce_typing
    def test_fail_return_str(arg_a: str) -> str:
        return int(arg_a)

    assert test_return_str(1) == "1"

    with pytest.raises(EnforcedTypingError):
        test_fail_return_str("1")


def test_enforce_typing_return_type_list():
    """Test the return type is an int."""

    @enforce_typing
    def test_return_list(arg_a: list) -> list:
        return arg_a

    @enforce_typing
    def test_fail_return_list(arg_a: list) -> list:
        return arg_a[0]

    assert test_return_list([1]) == [1]

    with pytest.raises(EnforcedTypingError):
        test_fail_return_list([1])


def test_enforce_typing_return_type_tuple():
    """Test the return type is an int."""

    @enforce_typing
    def test_return_tuple(arg_a: tuple) -> tuple:
        return arg_a

    @enforce_typing
    def test_fail_return_tuple(arg_a: tuple) -> tuple:
        return arg_a[0]

    assert test_return_tuple((1, 1)) == (1, 1)

    with pytest.raises(EnforcedTypingError):
        test_fail_return_tuple((1, 1))


def test_enforce_typing_return_type_dict():
    """Test the return type is an int."""

    @enforce_typing
    def test_return_dict(arg_a: dict) -> dict:
        return arg_a

    @enforce_typing
    def test_fail_return_dict(arg_a: dict) -> dict:
        return arg_a[1]

    assert test_return_dict({1: "1"}) == {1: "1"}

    with pytest.raises(EnforcedTypingError):
        test_fail_return_dict({1: "1"})
