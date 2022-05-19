"""Define the main interface to the CLI."""
import typer

from .commands.bookmark import BOOKMARK_APP
from .commands.tag import TAG_APP
from .helpers.logging import debug


def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Increase verbosity of standard output."
    ),
) -> None:
    """Interact with a linkding instance."""
    debug(ctx, f"Starting CLI with parameters: {ctx.params}")


APP = typer.Typer(callback=main)
APP.add_typer(BOOKMARK_APP, name="bookmarks", help="Manage bookmarks")
APP.add_typer(TAG_APP, name="tags", help="Manage tags")
