"""Test enforce typing module on Typing type hints."""  # pylint: disable=R0801
from typing import Dict, List, Tuple

import pytest

from .test_classes import User
from ..check_typing_types import CheckTyping
from ..enforce_typing import enforce_typing
from ..exceptions import EnforcedTypingError


def test_enforce_typing_dict():
    """Test the enforce_typing decorator with a Typing Dict."""

    @enforce_typing
    def test_dict(arg_a: Dict[str, int]) -> int:
        return list(arg_a.values())[0]

    assert test_dict({"index": 1})

    with pytest.raises(EnforcedTypingError):
        test_dict({"index": "1"})
    with pytest.raises(EnforcedTypingError):
        test_dict(("index", "1"))


def test_enforce_typing_list():
    """Test the enforce_typing decorator with a Typing List."""

    @enforce_typing
    def test_list(arg_a: List[int]) -> List[str]:
        return [str(i) for i in arg_a]

    assert test_list([1, 1, 1]) == ["1", "1", "1"]

    with pytest.raises(EnforcedTypingError):
        test_list([1, 1, 1, "1"])
    with pytest.raises(EnforcedTypingError):
        test_list((1, 1, 1, "1"))


def test_enforce_typing_tuple():
    """Test the enforce_typing decorator with a Typing Tuple."""

    @enforce_typing
    def test_tuple(arg_a: Tuple[int, int]) -> Tuple[int, str]:
        return (arg_a[0], str(arg_a[1]))

    assert test_tuple((4, 1)) == (4, "1")

    with pytest.raises(EnforcedTypingError):
        test_tuple(("4", 1))
    with pytest.raises(EnforcedTypingError):
        test_tuple(("4", 1, 1))
    with pytest.raises(EnforcedTypingError):
        test_tuple(["4", 1])


def test_validate():
    """
    Test the validate function.

    Always returns None, unless
    an exception is raised.
    """
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
        expected_type="List[int]",
    )
    assert test_typing_input.validate() is None

    test_bad_input = CheckTyping(
        arg_name="arg_a",
        arg_type=list,
        arg_value=[1, 1, 1],
        expected_type="typing.List[str]",
    )
    with pytest.raises(EnforcedTypingError):
        test_bad_input.validate()


def test_split_typing_sub_types():
    """Test the function to extract sub-types from a Typing type hint."""
    assert CheckTyping.split_typing_sub_types(
        str(Dict[str, User]).split("typing.Dict")[1],
    ) == [str, User]

    assert CheckTyping.split_typing_sub_types(
        str(List[str]).split("typing.List")[1],
    ) == [str]

    assert CheckTyping.split_typing_sub_types(
        str(Tuple[str, User, int]).split("typing.Tuple")[1],
    ) == [str, User, int]
