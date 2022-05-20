"""Define the main interface to the CLI."""
from pathlib import Path
from typing import Optional

import typer

from .commands.bookmark import BOOKMARK_APP
from .commands.tag import TAG_APP
from .const import ENV_CONFIG, ENV_TOKEN, ENV_URL
from .core import LinkDing
from .errors import LinkDingCliError
from .helpers.logging import debug, error


def main(
    ctx: typer.Context,
    config: Optional[Path] = typer.Option(
        None,
        "--config",
        "-c",
        envvar=[ENV_CONFIG],
        exists=True,
        file_okay=True,
        dir_okay=False,
        help="A path to a config file.",
        metavar="PATH",
        resolve_path=True,
    ),
    token: Optional[str] = typer.Option(
        None,
        "--token",
        "-t",
        envvar=[ENV_TOKEN],
        help="A linkding API token.",
        metavar="TOKEN",
    ),
    url: Optional[str] = typer.Option(
        None,
        "--url",
        "-u",
        envvar=[ENV_URL],
        help="A URL to a linkding instance.",
        metavar="URL",
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
        ctx.obj = LinkDing(ctx.params)
    except LinkDingCliError as err:
        error(str(err))
        raise typer.Exit(code=1) from err

    debug(ctx, f"Starting CLI with config: {ctx.obj.config}")


APP = typer.Typer(callback=main)
APP.add_typer(BOOKMARK_APP, name="bookmarks", help="Manage bookmarks")
APP.add_typer(TAG_APP, name="tags", help="Manage tags")
