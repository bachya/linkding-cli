"""Define logging helpers."""
import typer


def debug(ctx: typer.Context, msg: str) -> None:
    """Log a debug message."""
    if not ctx.params["verbose"]:
        return
    typer.echo(f"DEBUG: {msg}")
