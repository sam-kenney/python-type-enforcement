# Python Staticly Typed Functions
Enforce type hints in functions by raising an `EnforcedTypingError` if there is a mismatch between type-hints and provided data types.


## Creating an environment
Create a virtual development environment by using the `virtualenv` Python library. You can install this by executing `pip install virtualenv`. 

To create your environment, type `virtualenv venv --prompt "(your-env) "`. Once created, you can activate it by using `source venv/bin/activate`. Once you are done developing, simply type `deactivate` in your terminal.


## Installation
### Using the library
*   Install this library by running `pip install git+ssh://github.com/mr-strawberry66/python-static-type-checking`. 
*   Import it to your code by adding `from enforce_typing import enforce_typing` to your file.

### Developing for this library
*   Install the required Python libraries using `pip install -r requirements.txt`.
*   If you are developing for this tool, install the Python libraries required by running `pip install -r dev-requirements.txt`.

*Please ensure to create your environment before you execute any of the installation commands*

## Using the decorator
The decorator can be used with both `functions` and `classes`, but must be the first decorator listed for each `function` or `class`. 
### Functions
```py
from typing import Dict, Tuple

from enforce_typing import enforce_typing


@enforce_typing
def foo(a: Dict[int, str]) -> str:
    return a.get(1)

foo({1: "Hello"})
# No errors

foo({"1": "Hello"}) 
# Will throw an EnforcedTypingError
# as the key is a str rather than an int


@enforce_typing
def bar(b: Tuple[int, int]) -> str:
    return b[1]

bar((1,2))
# No errors

bar((1,2,3))
# Will throw an EnforcedTypingError
# as the tuple is too large.
```

### Classes
This decorator supports both standard `Classes` and `dataclasses`. You may also add the decorator to any functions within a `Class`.
```py
from dataclasses import dataclass
from typing import Dict, List

from enforce_typing import enforce_typing

# dataclass implementation
@enforce_typing
@dataclass
class User:
    name: str
    age: int
    roles: List[str]

    @enforce_typing
    @staticmethod
    def foo(a: Dict[int, str]) -> str:
        return a.get(1)


# Standard implementation
@enforce_typing
class User:
    def __init__(
        self, name: str, age: int, roles: List[str]
    ) -> None:
        self.name = name
        self.age = age
        self.roles = roles

    @enforce_typing
    @staticmethod
    def foo(a: Dict[int, str]) -> str:
        return a.get(1)
```

### Strictness
#### **Built-in Types**
For the built-in types, such as `str`, `int`, `float` `bool`, `dict`, and `list`, the `EnforcedTypingError` will be thrown if the annotated type does not match the type of the variable at runtime.

#### **Typing Types**
For the advanced type hints available through the `typing` module, such as `Dict`, `List`, and `Tuple`, the annotation's sub-type (such as `List[str]`) will also be checked against the contents of the variable. 

In the case of `List[str]`, each item in the list will validated, if any items are not a `str`, the `EnforcedTypingError` will be thrown.

For `Dict`, the key and values of each pair in the `dict` will be compared to the sub-types in the function's annotations. For example, `Dict[int, str]` will make sure that each key is an `int`, and each value is a `str`.

For `Tuple`, as well as checking that each item in the `tuple` is the correct type, as per the function annotation, but also that the passed in `tuple` is the expected length. For example, `Tuple[str, int]`, would raise an error if you passed in `("Hi", 1, 2)`, as the passed in value has too many items.

#### **User Defined Types**
You may use your own `Classes` as type hints in your functions. For example.
```py
from typing import List

from enforce_typing import enforce_typing

from .my_module import MyClass


@enforce_typing
def foo(c: List[MyClass]) -> None:
    [print(i) for i in c]
```

#### **Any and Ellipsis**
The use of `any`, `typing.Any`, or `...` in your type annotations is not supported.
