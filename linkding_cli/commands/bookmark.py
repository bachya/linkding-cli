"""Define the bookmark command."""
from __future__ import annotations

import asyncio
import json

from aiolinkding.errors import LinkDingError
import typer

from linkding_cli.const import CONF_LIMIT, CONF_OFFSET, CONF_QUERY
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
    limit: int = typer.Option(
        None,
        "--limit",
        "-l",
        help="The number of bookmarks to return.",
    ),
    offset: int = typer.Option(
        None,
        "--offset",
        "-o",
        help="The index from which to return results.",
    ),
    query: str = typer.Option(
        None,
        "--query",
        "-q",
        help="Return bookmarks containing a query string.",
    ),
) -> None:
    """Get all bookmarks."""
    kwargs = {}

    for param, conf_key in (
        (limit, CONF_LIMIT),
        (offset, CONF_OFFSET),
        (query, CONF_QUERY),
    ):
        if param:
            kwargs[conf_key] = param

    if archived:
        func = ctx.obj.client.bookmarks.async_get_archived
    else:
        func = ctx.obj.client.bookmarks.async_get_all
    data = asyncio.run(func(**kwargs))
    typer.echo(json.dumps(data))


@log_exception(LinkDingError)
def get_by_id(
    ctx: typer.Context,
    bookmark_id: int = typer.Argument(
        None,
        help="The ID of a bookmark to retrieve.",
    ),
) -> None:
    """Get a bookmark by it's linkding ID."""
    data = asyncio.run(ctx.obj.client.bookmarks.async_get_single(bookmark_id))
    typer.echo(json.dumps(data))


BOOKMARK_APP = typer.Typer()
BOOKMARK_APP.command(name="all")(get_all)
BOOKMARK_APP.command(name="id")(get_by_id)
