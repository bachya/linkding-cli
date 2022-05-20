"""Define various decorators."""
from __future__ import annotations

from functools import wraps
from typing import Any, Callable, TypeVar

import typer

from .logging import error

T = TypeVar("T")


def log_exception(
    exc: type[Exception], *, exit_code: int = 1
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Define a dectorator to handle exceptions via typer output."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        """Decorate."""

        @wraps(func)
        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> T:
            """Wrap."""
            try:
                return func(*args, **kwargs)
            except exc as err:
                error(str(err))
                raise typer.Exit(code=exit_code) from err

        return wrapper

    return decorator
