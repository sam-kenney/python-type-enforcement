"""Test enforce typing module on __future__ type hints."""
from __future__ import annotations
import pytest

from .test_classes import User
from ..check_future_or_typing_types import CheckTyping
from ..enforce_typing import enforce_typing
from ..exceptions import EnforcedTypingError


def test_enforce_typing_dict():
    """Test the enforce_typing decorator with a __future__ dict."""

    @enforce_typing
    def test_dict(arg_a: dict[str, int]) -> int:
        return list(arg_a.values())[0]

    assert test_dict({"index": 1})

    with pytest.raises(EnforcedTypingError):
        test_dict({"index": "1"})
    with pytest.raises(EnforcedTypingError):
        test_dict(("index", "1"))


def test_enforce_typing_list():
    """Test the enforce_typing decorator with a __future__ list."""

    @enforce_typing
    def test_list(arg_a: list[int]) -> list[str]:
        return [str(i) for i in arg_a]

    assert test_list([1, 1, 1]) == ["1", "1", "1"]

    with pytest.raises(EnforcedTypingError):
        test_list([1, 1, 1, "1"])
    with pytest.raises(EnforcedTypingError):
        test_list((1, 1, 1, "1"))


def test_enforce_typing_tuple():
    """Test the enforce_typing decorator with a __future__ tuple."""

    @enforce_typing
    def test_tuple(arg_a: tuple[int, int]) -> tuple[int, str]:
        return (arg_a[0], str(arg_a[1]))

    assert test_tuple((4, 1)) == (4, "1")

    with pytest.raises(EnforcedTypingError):
        test_tuple(("4", 1))
    with pytest.raises(EnforcedTypingError):
        test_tuple(("4", 1, 1))
    with pytest.raises(EnforcedTypingError):
        test_tuple(["4", 1])


def test_return_typing_tuple():
    """Test the enforce_typing decorator returns a __future__ tuple."""

    @enforce_typing
    def test_return_tuple(arg_a: tuple[int, int]) -> tuple[str, str]:
        return (str(arg_a[0]), str(arg_a[1]))

    @enforce_typing
    def test_fail_return_tuple(arg_a: tuple[int, int]) -> tuple[str, str]:
        return arg_a[0]

    assert test_return_tuple((4, 1)) == ("4", "1")

    with pytest.raises(EnforcedTypingError):
        test_fail_return_tuple((4, 1))


def test_return_typing_list():
    """Test the enforce_typing decorator returns a __future__ list."""

    @enforce_typing
    def test_return_list(arg_a: list[int]) -> list[str]:
        return [str(arg_a[0]), str(arg_a[1])]

    @enforce_typing
    def test_fail_return_list(arg_a: list[int]) -> list[str]:
        return arg_a[0]

    assert test_return_list([4, 1]) == ["4", "1"]

    with pytest.raises(EnforcedTypingError):
        test_fail_return_list([4, 1])


def test_return_typing_dict():
    """Test the enforce_typing decorator returns a __future__ dict."""

    @enforce_typing
    def test_return_dict(arg_a: dict[int, str]) -> dict[str, str]:
        return {str(key): str(val) for key, val in arg_a.items()}

    @enforce_typing
    def test_fail_return_dict(arg_a: dict[int, str]) -> dict[int, str]:
        return arg_a[1]

    assert test_return_dict({1: "1"}) == {"1": "1"}

    with pytest.raises(EnforcedTypingError):
        test_fail_return_dict({1: "1"})


def test_validate():
    """Test the validate function."""
    test_non_typing_input = CheckTyping(
        arg_name="arg_a",
        arg_type=str,
        arg_value="1",
        expected_type="str",
    )
    assert test_non_typing_input.validate() is None

    test_typing_input = CheckTyping(
        arg_name="arg_a",
        arg_type=list,
        arg_value=[1, 1, 1],
        expected_type="list[int]",
    )
    assert test_typing_input.validate() is None

    test_bad_input = CheckTyping(
        arg_name="arg_a",
        arg_type=list,
        arg_value=[1, 1, 1],
        expected_type="typing.list[str]",
    )
    with pytest.raises(EnforcedTypingError):
        test_bad_input.validate()


def test_split_typing_sub_types():
    """Test the function to extract sub-types from a __future__ type hint."""
    assert CheckTyping.split_typing_sub_types(
        str([str.__qualname__, User.__qualname__]),
    ) == ["str", "User"]

    assert CheckTyping.split_typing_sub_types(
        str(list.__qualname__),
    ) == [list]

    assert CheckTyping.split_typing_sub_types(
        str(dict.__qualname__),
    ) == [dict]
