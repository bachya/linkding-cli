"""Define logging helpers."""
from __future__ import annotations

import logging
import traceback
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar, cast

import typer

from linkding_cli.const import LOGGER


class TyperLoggerHandler(logging.Handler):
    """Define a logging handler that works with Typer."""

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record.

        Args:
            record: The log record.
        """
        foreground = None
        if record.levelno == logging.CRITICAL:
            foreground = typer.colors.BRIGHT_RED
        elif record.levelno == logging.DEBUG:
            foreground = typer.colors.BRIGHT_BLUE
        elif record.levelno == logging.ERROR:
            foreground = typer.colors.BRIGHT_RED
        elif record.levelno == logging.INFO:
            foreground = typer.colors.BRIGHT_GREEN
        elif record.levelno == logging.WARNING:
            foreground = typer.colors.BRIGHT_YELLOW
        typer.secho(self.format(record), fg=foreground)


_T = TypeVar("_T")
_CallableThatFailsType = Callable[..., _T]


def log_exception(
    *, exit_code: int = 1
) -> Callable[[_CallableThatFailsType], _CallableThatFailsType]:
    """Define a dectorator to handle exceptions via typer output.

    Args:
        exit_code: The code to exit with upon exception.

    Returns:
        The decorated callable.
    """

    def decorator(func: _CallableThatFailsType) -> _CallableThatFailsType:
        """Decorate.

        Args:
            func: The callable to decorate.

        Returns:
            The decorated callable.
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: dict[str, Any]) -> dict[str, Any]:
            """Wrap.

            Args:
                args: The callable's arguments.
                kwargs: The callable's keyword arguments.

            Returns:
                The original callable's return type.

            Raises:
                Exit: Raised when the command fails in any way.
            """
            try:
                return cast(dict[str, Any], func(*args, **kwargs))
            except Exception as err:  # pylint: disable=broad-except
                LOGGER.error(err)
                LOGGER.debug("".join(traceback.format_tb(err.__traceback__)))
                raise typer.Exit(code=exit_code) from err

        return wrapper

    return decorator
