"""Check stdlib type hints without __future__ annotations, or use of Typing lib."""
from __future__ import annotations

from .exceptions import EnforcedTypingError
from .type_parser import data_type_from_string


def check_builtin_types(
    arg_name: str,
    arg_type: any,
    func_arg_types: dict[any, any],
):
    """
    Test to see if type hints used with stdlib types are correct.

    Args:
        arg: str
            The argument name.

        arg_type: any
            The datatype of the argument.

        func_arg_types: dict[any, any]
            The type hints applied to the variables
            of the function.

    Raises: EnforcedTypingError
        If the data does not match
        the datatype of the type
        hint.
    """
    if isinstance(func_arg_types[arg_name], str):
        data_type = func_arg_types[arg_name]

    else:
        data_type = str(func_arg_types[arg_name].__qualname__)

    received_arg_type = data_type_from_string(data_type)
    if not issubclass(arg_type, received_arg_type):
        raise EnforcedTypingError(
            f"'{arg_name}' is a {arg_type}"
            f", but should be {func_arg_types[arg_name]}."
        )
