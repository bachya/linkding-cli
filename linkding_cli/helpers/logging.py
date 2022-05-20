"""Define logging helpers."""
from __future__ import annotations

import typer


def error(msg: str) -> None:
    """Log an error message."""
    typer.echo(f"Error: {msg}", err=True)


def debug(ctx: typer.Context, msg: str) -> None:
    """Log a debug message."""
    if not ctx.obj.config.verbose:
        return
    typer.echo(f"Debug: {msg}")
