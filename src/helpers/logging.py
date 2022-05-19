"""Define logging helpers."""
from __future__ import annotations

import typer

from src.const import CONF_VERBOSE


def error(msg: str) -> None:
    """Log an error message."""
    typer.secho(f"ERROR: {msg}", fg=typer.colors.RED)


def debug(ctx: typer.Context, msg: str) -> None:
    """Log a debug message."""
    if not ctx.obj.params[CONF_VERBOSE]:
        return
    typer.secho(f"DEBUG: {msg}", fg=typer.colors.BLUE)
