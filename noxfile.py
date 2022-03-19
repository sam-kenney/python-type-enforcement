"""Nox configuration Lint and Test code."""
import nox


@nox.session
def lint(session):
    """Lint using flake8."""
    session.install(
        "flake8",
        "flake8-docstrings",
        "flake8-import-order",
        "pylint",
    )
    session.install("-r", "dev-requirements.txt")
    session.run("flake8", "--max-complexity=8")
    session.run("pylint", "./enforce_typing/")


@nox.session
def format(session):
    """Format using black."""
    session.install("black")
    session.run("black", ".")


@nox.session
def test(session):
    """Run tests."""
    session.install("pytest")
    session.install("pytest-cov")
    session.run(
        "pytest",
        "--cov=enforce_typing",
        "--cov-report",
        "term-missing",
    )
