"""Define configuration management."""
from __future__ import annotations

from typing import cast

import typer
from ruamel.yaml import YAML

from linkding_cli.const import CONF_TOKEN, CONF_URL, CONF_VERBOSE, LOGGER
from linkding_cli.errors import ConfigError

CONF_CONFIG = "config"


class Config:
    """Define the config manager object."""

    def __init__(self, ctx: typer.Context) -> None:
        """Initialize.

        Args:
            ctx: A Typer Context object.

        Raises:
            ConfigError: Raised upon invalid config
        """
        LOGGER.debug("Command: %s", ctx.invoked_subcommand)
        LOGGER.debug("Arguments: %s", ctx.args)
        LOGGER.debug("Options: %s", ctx.params)

        self._config = {}

        # If the user provides a config file, attempt to load it:
        if config_path := ctx.params[CONF_CONFIG]:
            parser = YAML(typ="safe")
            with open(config_path, encoding="utf-8") as config_file:
                self._config = parser.load(config_file)

        if not isinstance(self._config, dict):
            raise ConfigError(f"Unable to parse config file: {config_path}")

        # Merge the CLI options/environment variables in using this logic:
        #   1. If the value is not None, its an override and we should use it
        #   2. If a key doesn't exist in self._config yet, include it
        for key, value in ctx.params.items():
            if value is not None or key not in self._config:
                self._config[key] = value

        # If, after all the configuration loading, we don't have a URL or a token, we
        # can't proceed:
        for param in (CONF_TOKEN, CONF_URL):
            if not self._config[param]:
                raise ConfigError(f"Missing required option: --{param}")

        LOGGER.debug("Loaded Config: %s", self)

    def __str__(self) -> str:
        """Define the string representation.

        Returns:
            A string representation.
        """
        return f"<Config token={self.token} url={self.url} verbose={self.verbose}>"

    @property
    def token(self) -> str:
        """Return the linkding API token.

        Returns:
            The linkding API token.
        """
        return cast(str, self._config[CONF_TOKEN])

    @property
    def url(self) -> str:
        """Return the linkding URL.

        Returns:
            The linkding API token.
        """
        return cast(str, self._config[CONF_URL])

    @property
    def verbose(self) -> bool:
        """Return the verbosity level.

        Returns:
            The verbosity level.
        """
        return cast(bool, self._config[CONF_VERBOSE])
