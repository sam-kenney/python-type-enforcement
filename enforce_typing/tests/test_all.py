"""Test enforce typing module."""
from typing import Dict, List, Tuple

import pytest

from ..enforce_typing import enforce_typing
from ..exceptions import EnforcedTypingError


def test_enforce_typing_Dict():
    """Test the enforce_typing decorator with a Typing Dict."""

    @enforce_typing
    def test_Dict(a: Dict[str, int]) -> int:
        return list(a.values())[0]

    assert test_Dict({"index": 1})

    with pytest.raises(EnforcedTypingError):
        test_Dict({"index": "1"})
    with pytest.raises(EnforcedTypingError):
        test_Dict(("index", "1"))


def test_enforce_typing_List():
    """Test the enforce_typing decorator with a Typing List."""

    @enforce_typing
    def test_List(a: List[int]) -> List[str]:
        return [str(i) for i in a]

    assert test_List([1, 1, 1]) == ["1", "1", "1"]

    with pytest.raises(EnforcedTypingError):
        test_List([1, 1, 1, "1"])
    with pytest.raises(EnforcedTypingError):
        test_List((1, 1, 1, "1"))


def test_enforce_typing_Tuple():
    """Test the enforce_typing decorator with a Typing Tuple."""

    @enforce_typing
    def test_Tuple(a: Tuple[int, int]) -> Tuple[int, str]:
        return (a[0], str(a[1]))

    assert test_Tuple((4, 1)) == (4, "1")

    with pytest.raises(EnforcedTypingError):
        test_Tuple(("4", 1))
    with pytest.raises(EnforcedTypingError):
        test_Tuple(("4", 1, 1))
    with pytest.raises(EnforcedTypingError):
        test_Tuple(["4", 1])


def test_enforce_typing_dict():
    """Test the enforce_typing decorator with a std dict."""

    @enforce_typing
    def test_list(a: dict) -> str:
        return list(a.values())[0]

    assert test_list({"index": "1"}) == "1"

    with pytest.raises(EnforcedTypingError):
        test_list({"index": 1})
    with pytest.raises(EnforcedTypingError):
        test_list((1, "1"))


def test_enforce_typing_list():
    """Test the enforce_typing decorator with a std list."""

    @enforce_typing
    def test_list(a: list) -> str:
        return a[0]

    assert test_list(["1", 1]) == "1"

    with pytest.raises(EnforcedTypingError):
        test_list([1, "1"])
    with pytest.raises(EnforcedTypingError):
        test_list((1, "1"))


def test_enforce_typing_tuple():
    """Test the enforce_typing decorator with a std tuple."""

    @enforce_typing
    def test_list(a: tuple) -> str:
        return a[0]

    assert test_list(("1", 1)) == "1"

    with pytest.raises(EnforcedTypingError):
        test_list((1, 1))
    with pytest.raises(EnforcedTypingError):
        test_list([1, 1])
