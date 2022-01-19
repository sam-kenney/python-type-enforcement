"""Setup config for Now CLI."""

from setuptools import find_packages, setup

setup(
    packages=["enforce_typing"]
    + ["enforce_typing." + pkg for pkg in find_packages("enforce_typing")],
)
