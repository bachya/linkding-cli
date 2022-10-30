"""Define the main interface to the CLI."""
# pylint: disable=unused-argument
from __future__ import annotations

from pathlib import Path

import typer

from linkding_cli.commands.bookmark import BOOKMARK_APP
from linkding_cli.commands.tag import TAG_APP
from linkding_cli.const import ENV_CONFIG, ENV_TOKEN, ENV_URL
from linkding_cli.core import LinkDing
from linkding_cli.helpers.logging import log_exception


@log_exception()
def main(
    ctx: typer.Context,
    config: Path = typer.Option(
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
    token: str = typer.Option(
        None,
        "--token",
        "-t",
        envvar=[ENV_TOKEN],
        help="A linkding API token.",
        metavar="TOKEN",
    ),
    url: str = typer.Option(
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
    """Interact with a linkding instance.

    Args:
        ctx: A Typer Context object.
        config: A path to a config file
        token: A linkding API token.
        url: A URL to a linkding instance.
        verbose: Increase verbosity of standard output.
    """
    ctx.obj = LinkDing(ctx)


APP = typer.Typer(callback=main)
APP.add_typer(BOOKMARK_APP, name="bookmarks", help="Work with bookmarks.")
APP.add_typer(TAG_APP, name="tags", help="Work with tags.")
