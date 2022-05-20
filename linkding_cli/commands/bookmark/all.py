"""Define the bookmarks all command."""
import asyncio
import json

from aiolinkding.errors import LinkDingError
import typer

from linkding_cli.helpers.decorator import log_exception


@log_exception(LinkDingError)
def get_all(ctx: typer.Context) -> None:
    """Get all bookmarks."""
    data = asyncio.run(ctx.obj.client.bookmarks.async_get_all())
    typer.echo(json.dumps(data))


BOOKMARK_ALL_APP = typer.Typer()
BOOKMARK_ALL_APP.callback(invoke_without_command=True)(get_all)
BOOKMARK_ALL_APP.command(name="all")(get_all)
