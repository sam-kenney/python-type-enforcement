"""Module used to enforce strict typing for Python functions."""
import re
from typing import Dict, List, Tuple, get_type_hints


class EnforcedTypingError(TypeError):
    """Class to raise errors relating to static typing decorator."""


def _check_argument_types(
    func_args: dict,
    func_arg_types: dict,
):
    """
    Check that the variables passed into a function are of the correct type.

    args:
        func_args: dict
            The arguments passed into a function
            when called.

        func_arg_types: dict
            The type hints applied to the variables
            of the function.
    """
    for arg_name, arg_value in [(key, value) for key, value in func_args.items()]:
        if arg_name in func_arg_types:
            if type(func_arg_types[arg_name]).__qualname__ == "_GenericAlias":
                _check_typing_types(
                    arg_name=arg_name,
                    arg_type=type(arg_value),
                    arg_value=arg_value,
                    expected_type=(str(func_arg_types[arg_name])),
                )

            else:
                _check_builtin_types(
                    arg_name=arg_name,
                    arg_type=type(arg_value),
                    func_arg_types=func_arg_types,
                )


def _check_typing_types(
    arg_name: str,
    arg_type: str,
    arg_value: any,
    expected_type: str,
):
    """
    Test to see if type hints used with typing types are correct.

    args:
        arg: str
            The argument name.

        arg_type: any
            The datatype of the argument.

        arg_value: any
            The value of the argument.

        expected_type: str
            The datatype type hinted at the
            function definition.
    """
    try:
        rx = re.search(r"typing\.([A-z].*)(\[.*])", expected_type)
        base_type: str = rx.group(1)
        sub_types: List[any] = _split_typing_sub_types(rx.group(2))

        if base_type == "Dict":
            if arg_type == dict:
                _check_typing_dict(
                    arg_name=arg_name,
                    arg_value=arg_value,
                    sub_types=sub_types,
                )
            else:
                raise EnforcedTypingError(
                    f"Argument '{arg_name}' is a {type(arg_value).__qualname__} "
                    f"but should be a {expected_type}"
                )

        elif base_type == "List":
            if arg_type == list:
                _check_typing_list(
                    arg_name=arg_name,
                    arg_value=arg_value,
                    sub_types=sub_types,
                )
            else:
                raise EnforcedTypingError(
                    f"'{arg_name}' is a {type(arg_value).__qualname__} "
                    f"but should be a {expected_type}"
                )

        elif base_type == "Tuple":
            if arg_type == tuple:
                _check_typing_tuple(
                    arg_name=arg_name,
                    arg_value=arg_value,
                    sub_types=sub_types,
                )
            else:
                raise EnforcedTypingError(
                    f"'{arg_name}' is a {type(arg_value).__qualname__} "
                    f"but should be a {expected_type}"
                )

    except AttributeError:
        return


def _split_typing_sub_types(sub_types: str) -> List[any]:
    """Convert sub_types from a string to a list."""
    return eval(sub_types)


def _check_typing_dict(arg_name: str, arg_value: Dict[any, any], sub_types: List[any]):
    """
    Check that the typed values for a dict match the values provided.

    args:
        arg_name: str
            The name of the argument.

        arg_value: Dict[any, any]
            The value of the provided argument.

        sub_types: List[any]
            The specified types within the
            typing Dict type hint.
    """
    typed_key, typed_value = sub_types
    for key, value in arg_value.items():
        if typed_key != type(key) or typed_value != type(value):
            raise EnforcedTypingError(
                f"'{arg_name}' has a key type of {type(key).__qualname__} "
                f"and a value type of {type(value).__qualname__}.\n"
                f"Should have a key type of {typed_key.__qualname__} "
                f"and a value type of {typed_value.__qualname__}."
            )


def _check_typing_list(
    arg_name: str,
    arg_value: List[any],
    sub_types: List[any],
):
    """
    Check that the typed value for a list match the values provided.

    args:
        arg_name: str
            The name of the argument.

        arg_value: List[any]
            The value of the provided argument.

        sub_types: List[any]
            The specified type within the
            typing List type hint.
    """
    for i, item in enumerate(arg_value):
        if type(item) != sub_types[0]:
            raise EnforcedTypingError(
                f"'{arg_name}' has a {type(item).__qualname__} at index {i}"
                f", but should be {sub_types[0].__qualname__}."
            )


def _check_typing_tuple(
    arg_name: str,
    arg_value: Tuple[any, ...],
    sub_types: List[any],
):
    """
    Check that the typed values for a tuple match the values provided.

    args:
        arg_name: str
            The name of the argument.

        arg_value: Tuple[any]
            The value of the provided argument.

        sub_types: List[any]
            The specified types within the
            typing Tuple type hint.
    """
    if len(arg_value) != len(sub_types):
        raise EnforcedTypingError(
            f"'{arg_name}' has a length of {len(arg_value)}"
            f", but should be a length of {len(sub_types)}."
        )

    for i, (item, sub_type) in enumerate(zip(arg_value, sub_types)):
        if type(item) != sub_type:
            raise EnforcedTypingError(
                f"'{arg_name}' has a {type(item).__qualname__} at index {i}"
                f", but should be {sub_type.__qualname__}."
            )


def _check_builtin_types(
    arg_name: str,
    arg_type: any,
    func_arg_types: dict,
):
    """
    Test to see if type hints used with stdlib types are correct.

    args:
        arg: str
            The argument name.

        arg_type: any
            The datatype of the argument.

        func_arg_types: dict
            The type hints applied to the variables
            of the function.
    """
    if not issubclass(arg_type, func_arg_types[arg_name]):
        raise EnforcedTypingError(
            f"'{arg_name}' is a {arg_type.__qualname__}"
            f", but should be {func_arg_types[arg_name].__qualname__}."
        )


def _check_return_types(
    func_arg_types: dict,
    return_type: any,
    return_value: any,
):
    """
    Check that the returned objectof a function is of the correct type.

    args:
        func_arg_types: dict
            The type hints applied to the variables
            of the function.

        return_type: any
            The return type hint of the function.

        return_value: any
            The returned value of the function.
    """
    if "return" in func_arg_types:
        if type(func_arg_types["return"]).__qualname__ == "_GenericAlias":
            _check_typing_types(
                arg_name="return value",
                arg_type=return_type,
                arg_value=return_value,
                expected_type=(str(func_arg_types["return"])),
            )

        else:
            _check_builtin_types(
                arg_name="return value",
                arg_type=return_type,
                func_arg_types=func_arg_types,
            )


def enforce_typing(func):
    """Enforce variable types."""

    def type_checker(*args, **kwargs):
        """Test argument vs value types."""
        func_type_hints = get_type_hints(func)
        arguments = kwargs.copy()
        arguments.update(zip(func.__code__.co_varnames, args))

        _check_argument_types(
            func_args=arguments,
            func_arg_types=func_type_hints,
        )

        function_result = func(*args, **kwargs)

        _check_return_types(
            func_arg_types=func_type_hints,
            return_type=type(function_result),
            return_value=function_result,
        )

        return function_result

    return type_checker
