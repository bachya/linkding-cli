"""Define configuration management."""
from __future__ import annotations

from typing import Any, cast

from ruamel.yaml import YAML

from linkding_cli.const import CONF_TOKEN, CONF_URL, CONF_VERBOSE
from linkding_cli.errors import ConfigError

CONF_CONFIG = "config"


class Config:
    """Define the config manager object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        self._config = {}

        # If the user provides a config file, attempt to load it:
        if config_path := params[CONF_CONFIG]:
            parser = YAML(typ="safe")
            with open(config_path, encoding="utf-8") as config_file:
                self._config = parser.load(config_file)

        if not isinstance(self._config, dict):
            raise ConfigError(f"Unable to parse config file: {config_path}")

        # Merge the CLI options/environment variables in using this logic:
        #   1. If the value is not None, its an override and we should use it
        #   2. If a key doesn't exist in self._config yet, include it
        for key, value in params.items():
            if value is not None or key not in self._config:
                self._config[key] = value

        # If, after all the configuration loading, we don't have a URL or a token, we
        # can't proceed:
        for param in (CONF_TOKEN, CONF_URL):
            if not self._config[param]:
                raise ConfigError(f"Missing required option: --{param}")

    def __str__(self) -> str:
        """Define the string representation."""
        return f"<Config token={self.token} url={self.url} verbose={self.verbose}>"

    @property
    def token(self) -> str:
        """Return the linkding token."""
        return cast(str, self._config[CONF_TOKEN])

    @property
    def url(self) -> str:
        """Return the linkding URL."""
        return cast(str, self._config[CONF_URL])

    @property
    def verbose(self) -> bool:
        """Return the verbosity level."""
        return cast(bool, self._config[CONF_VERBOSE])
