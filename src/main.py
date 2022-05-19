"""Define the main interface to the CLI."""
import typer

from .commands.bookmark import BOOKMARK_APP
from .commands.tag import TAG_APP
from .const import ENV_TOKEN, ENV_URL
from .data import Data
from .errors import LinkDingCliError
from .helpers.logging import debug, error


def main(
    ctx: typer.Context,
    url: str = typer.Option(
        None,
        "--url",
        "-u",
        help="A URL to a linkding instance.",
        envvar=[ENV_URL],
        metavar="URL",
    ),
    token: str = typer.Option(
        None,
        "--token",
        "-t",
        help="A linkding API token.",
        envvar=[ENV_TOKEN],
        metavar="TOKEN",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Increase verbosity of standard output.",
    ),
) -> None:
    """Interact with a linkding instance."""
    try:
        ctx.obj = Data(ctx.params)
    except LinkDingCliError as err:
        error(str(err))
        raise typer.Exit(code=1) from err

    debug(ctx, f"Starting CLI with parameters: {ctx.params}")


APP = typer.Typer(callback=main)
APP.add_typer(BOOKMARK_APP, name="bookmarks", help="Manage bookmarks")
APP.add_typer(TAG_APP, name="tags", help="Manage tags")
