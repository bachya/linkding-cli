"""Define the user command."""
from __future__ import annotations

import asyncio
import json

import typer

from linkding_cli.helpers.logging import log_exception


@log_exception()
def get_profile_info(ctx: typer.Context) -> None:
    """Get all tags.

    Args:
        ctx: A Typer Context object.
    """
    data = asyncio.run(ctx.obj.client.user.async_get_profile())
    typer.echo(json.dumps(data))


@log_exception()
def main(_: typer.Context) -> None:
    """Interact with user info."""
    pass


USER_APP = typer.Typer(callback=main)
USER_APP.command(name="profile")(get_profile_info)
