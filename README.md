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
```py
from typing import Dict, Tuple

from enforce_typing import enforce_typing


@enforce_typing
def foo(a: Dict[int: str]) -> str:
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

### Strictness
#### str
Will throw an error if the value passed in to the function is not a `string`, or subclass of `string`.

### int
Will throw an error if the value passed in to the function is not an `int`, or subclass of `int`.

### float
Will throw an error if the value passed in to the function is not a `float`, or subclass of `float`.

### list / typing.List
Standard `list`s will only check for type equality. If you are using `typing` annotations, it will check that the sub-types are correct too. For example, annotating `List[str]` will check that each item in the `list` is a `str`.

### dict / typing.Dict
Standard `dict`s will only check for type equality. If you are using `typing` annotations, it will check that the sub-types are correct too. For example, annotating `Dict[str, int]` will check that each key-value pair in the dictionary have a `str` key, and an `int` value.

### tuple / typing.Tuple
Standard `tuple`s will only check for type equality. If you are using `typing` annotations, it will check that the sub-types are correct too. For example, annotating `Tuple[str, int, int]` will check that the passed in `tuple` is has the correct number of values, as well as each value in each position is the correct data type.
