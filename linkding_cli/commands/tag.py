"""Define the tag command."""
from __future__ import annotations

import asyncio
import json

import typer

from linkding_cli.const import CONF_LIMIT, CONF_OFFSET
from linkding_cli.helpers.logging import log_exception
from linkding_cli.util import generate_api_payload


@log_exception()
def create(
    ctx: typer.Context,
    tag_name: str = typer.Argument(..., help="The tag to create."),
) -> None:
    """Create a tag.

    Args:
        ctx: A Typer Context object.
        tag_name: The tag to create.
    """
    data = asyncio.run(ctx.obj.client.tags.async_create(tag_name))
    typer.echo(json.dumps(data))


@log_exception()
def get_all(
    ctx: typer.Context,
    limit: int = typer.Option(
        None,
        "--limit",
        "-l",
        help="The number of tags to return.",
    ),
    offset: int = typer.Option(
        None,
        "--offset",
        "-o",
        help="The index from which to return results.",
    ),
) -> None:
    """Get all tags.

    Args:
        ctx: A Typer Context object.
        limit: The number of tags to return.
        offset: The index from which to return results.
    """
    api_kwargs = generate_api_payload(
        (
            (CONF_LIMIT, limit),
            (CONF_OFFSET, offset),
        )
    )

    data = asyncio.run(ctx.obj.client.tags.async_get_all(**api_kwargs))
    typer.echo(json.dumps(data))


@log_exception()
def get_by_id(
    ctx: typer.Context,
    tag_id: int = typer.Argument(..., help="The ID of a tag to retrieve."),
) -> None:
    """Get a tag by its linkding ID.

    Args:
        ctx: A Typer Context object.
        tag_id: The ID of a tag to retrieve.
    """
    data = asyncio.run(ctx.obj.client.tags.async_get_single(tag_id))
    typer.echo(json.dumps(data))


@log_exception()
def main(_: typer.Context) -> None:
    """Interact with tags."""
    pass


TAG_APP = typer.Typer(callback=main)
TAG_APP.command(name="all")(get_all)
TAG_APP.command(name="create")(create)
TAG_APP.command(name="get")(get_by_id)
