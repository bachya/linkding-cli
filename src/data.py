"""Define a data object."""
from __future__ import annotations

from typing import Any

from .const import CONF_TOKEN, CONF_URL
from .errors import ConfigError


class Data:
    """Define a config manager object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        if not params[CONF_TOKEN]:
            raise ConfigError("Missing required option: token")
        if not params[CONF_URL]:
            raise ConfigError("Missing required option: url")

        self.params = params
