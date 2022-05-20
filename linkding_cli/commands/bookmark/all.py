"""Define the bookmarks all command."""
from __future__ import annotations

import asyncio
import json
from typing import Any

from aiolinkding.errors import LinkDingError
import typer

from linkding_cli.const import CONF_LIMIT, CONF_OFFSET, CONF_QUERY
from linkding_cli.helpers.decorator import log_exception


async def async_get_all_bookmarks() -> dict[str, Any]:
    """Get all bookmarks."""


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
        coro = ctx.obj.client.bookmarks.async_get_archived(**kwargs)
    else:
        coro = ctx.obj.client.bookmarks.async_get_all(**kwargs)
    data = asyncio.run(coro)
    typer.echo(json.dumps(data))


BOOKMARK_ALL_APP = typer.Typer()
BOOKMARK_ALL_APP.callback(invoke_without_command=True)(get_all)
