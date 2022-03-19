"""Convert class __qualname__ to class object."""
from __future__ import annotations

import importlib
import sys


def data_type_from_string(data_type: str, name_space: dict[str, any] = None) -> any:
    """
    Convert string repr of datatype to class.

    Args:
        data_type: str
            The string representation
            of the datatype.

    Returns: any
        The class of the datatype.
    """
    _name_space = name_space or {}

    try:
        lib = importlib.__import__(data_type.split(".")[0])
        _name_space.__setitem__(lib.__name__, lib)

    except ModuleNotFoundError:
        pass
    except AttributeError:
        pass

    data_type_as_class = eval(  # pylint: disable=W0123
        data_type,
        sys.modules,
        name_space,
    )
    return data_type_as_class
