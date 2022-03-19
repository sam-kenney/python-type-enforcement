"""Test enforce typing module on __future__ type hints."""  # pylint: disable=R0801
from __future__ import annotations

import pytest

from .test_classes import User
from ..type_parser import data_type_from_string


def test_data_type_from_string():
    """Test conversion of class repr to class."""
    assert data_type_from_string("int") == int
    assert data_type_from_string("str") == str
    assert data_type_from_string("dict") == dict
    assert data_type_from_string("list") == list
    assert data_type_from_string("tuple") == tuple
    assert data_type_from_string("enforce_typing.tests.test_classes.User") == User

    with pytest.raises(TypeError):
        data_type_from_string(User)
