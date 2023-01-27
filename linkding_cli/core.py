"""Define a data object."""
from __future__ import annotations

import logging

import typer
from aiolinkding import Client, async_get_client

from linkding_cli.config import Config
from linkding_cli.const import CONF_VERBOSE
from linkding_cli.helpers.logging import TyperLoggerHandler


class LinkDing:  # pylint: disable=too-few-public-methods
    """Define a master linkding manager object."""

    def __init__(self, ctx: typer.Context) -> None:
        """Initialize.

        Args:
            ctx: A Typer Context object.
        """
        if ctx.params[CONF_VERBOSE]:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        typer_handler = TyperLoggerHandler()
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
            handlers=(typer_handler,),
        )

        # We ignore the typing on self.client because (a) it will be assigned in
        # async_start and (b) this will help us avoid a bunch of type checks down the
        # line:
        self.client: Client = None  # type: ignore[assignment]
        self.config = Config(ctx)

    async def async_init(self) -> None:
        """Perform some post instantiation init."""
        self.client = await async_get_client(self.config.url, self.config.token)
