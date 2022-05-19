"""Define tag commands."""
import typer

BOOKMARK_APP = typer.Typer()


def get_all() -> None:
    """Get all bookmarks."""
    typer.echo("PLACEHOLDER")


BOOKMARK_APP.command(name="all")(get_all)
