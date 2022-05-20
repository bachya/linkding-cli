"""Define the bookmarks all command."""
import asyncio
import json

from aiolinkding.errors import LinkDingError
import typer

from linkding_cli.helpers.decorator import log_exception


@log_exception(LinkDingError)
def get_all(
    ctx: typer.Context,
    archived: bool = typer.Option(
        False,
        "--archived",
        "-a",
        help="Return archived bookmarks.",
    ),
) -> None:
    """Get all bookmarks."""
    if archived:
        coro = ctx.obj.client.bookmarks.async_get_archived()
    else:
        coro = ctx.obj.client.bookmarks.async_get_all()
    data = asyncio.run(coro)
    typer.echo(json.dumps(data))


BOOKMARK_ALL_APP = typer.Typer()
BOOKMARK_ALL_APP.callback(invoke_without_command=True)(get_all)
