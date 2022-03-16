"""Module for classes used in testing."""
from dataclasses import dataclass


@dataclass
class User:
    """Example class for testing purposes."""

    name: str
    age: int
