"""Define a data object."""
from __future__ import annotations

import logging

import typer
from aiolinkding import Client

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

        self.config = Config(ctx)
        self.client = Client(self.config.url, self.config.token)
