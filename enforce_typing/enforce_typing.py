"""Module used to enforce strict typing for Python functions."""
from __future__ import annotations

import inspect
import typing

from .check_builtin_types import check_builtin_types
from .check_typing_types import CheckTyping


def _check_argument_types(
    func_args: dict[any, any],
    func_arg_types: dict[any, any],
):
    """
    Check that the variables passed into a function are of the correct type.

    Args:
        func_args: dict[any, any]
            The arguments passed into a function
            when called.

        func_arg_types: dict[any, any]
            The type hints applied to the variables
            of the function.
    """
    for arg_name, arg_value in [(key, value) for key, value in func_args.items()]:
        if arg_name in func_arg_types:
            if type(func_arg_types[arg_name]).__qualname__ == "_GenericAlias":
                CheckTyping(
                    arg_name=arg_name,
                    arg_type=type(arg_value),
                    arg_value=arg_value,
                    expected_type=(str(func_arg_types[arg_name])),
                ).validate()

            else:
                check_builtin_types(
                    arg_name=arg_name,
                    arg_type=type(arg_value),
                    func_arg_types=func_arg_types,
                )


def _check_return_types(
    func_arg_types: dict[any, any],
    return_type: any,
    return_value: any,
):
    """
    Check that the returned objectof a function is of the correct type.

    Args:
        func_arg_types: dict[any, any]
            The type hints applied to the variables
            of the function.

        return_type: any
            The return type hint of the function.

        return_value: any
            The returned value of the function.
    """
    if "return" in func_arg_types:
        if type(func_arg_types["return"]).__qualname__ == "_GenericAlias":
            CheckTyping(
                arg_name="return",
                arg_type=return_type,
                arg_value=return_value,
                expected_type=(str(func_arg_types["return"])),
            ).validate()

        else:
            check_builtin_types(
                arg_name="return",
                arg_type=return_type,
                func_arg_types=func_arg_types,
            )


def enforce_typing(func: callable):
    """Enforce variable types."""

    def type_checker(*args, **kwargs):
        """Test argument vs value types."""
        arguments = kwargs.copy()
        if inspect.isclass(func):
            try:
                func_type_hints = typing.get_type_hints(func)
                arguments.update(zip(func.__annotations__, args))

            except AttributeError:
                func_type_hints = typing.get_type_hints(func.__init__)
                if func_type_hints.get("return", None):
                    func_type_hints["return"] = func
                arguments.update(zip(func_type_hints, args))

        else:
            func_type_hints = typing.get_type_hints(func)
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
