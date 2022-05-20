"""Define a data object."""
from __future__ import annotations

from typing import Any

from aiolinkding import Client

from linkding_cli.config import Config


class LinkDing:  # pylint: disable=too-few-public-methods
    """Define a master linkding manager object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        self.config = Config(params)
        self.client = Client(self.config.url, self.config.token)
