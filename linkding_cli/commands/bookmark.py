"""Define tag commands."""
import asyncio
import json

from aiolinkding.errors import LinkDingError
import typer

from linkding_cli.helpers.decorator import log_exception

BOOKMARK_APP = typer.Typer()


@log_exception(LinkDingError)
def get_all(ctx: typer.Context) -> None:
    """Get all bookmarks."""
    data = asyncio.run(ctx.obj.client.bookmarks.async_get_all())
    typer.echo(json.dumps(data))


BOOKMARK_APP.command(name="all")(get_all)
