"""Define the main interface to the CLI."""
from pathlib import Path
from typing import Optional

import typer

from linkding_cli.commands.bookmark import BOOKMARK_APP
from linkding_cli.commands.tag import TAG_APP
from linkding_cli.const import ENV_CONFIG, ENV_TOKEN, ENV_URL
from linkding_cli.core import LinkDing
from linkding_cli.errors import LinkDingCliError
from linkding_cli.helpers.decorator import log_exception
from linkding_cli.helpers.logging import debug


@log_exception(LinkDingCliError)
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
    ctx.obj = LinkDing(ctx.params)
    debug(ctx, f"Starting CLI with config: {ctx.obj.config}")
    debug(ctx, f"About to execute command: {ctx.invoked_subcommand}")


APP = typer.Typer(callback=main)
APP.add_typer(BOOKMARK_APP, name="bookmarks", help="Work with bookmarks.")
APP.add_typer(TAG_APP, name="tags", help="Work with tags.")
