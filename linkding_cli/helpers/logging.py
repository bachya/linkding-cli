"""Define logging helpers."""
from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

import typer

T = TypeVar("T")


def error(msg: str) -> None:
    """Log an error message."""
    typer.echo(f"Error: {msg}", err=True)


def debug(msg: str) -> None:
    """Log a debug message."""
    typer.echo(f"Debug: {msg}")


def log_exception(
    *, exit_code: int = 1
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Define a dectorator to handle exceptions via typer output."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """Decorate."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> T:
            """Wrap."""
            try:
                return func(*args, **kwargs)
            except Exception as err:  # pylint: disable=broad-except
                error(str(err))
                raise typer.Exit(code=exit_code) from err

        return wrapper

    return decorator
