"""Define package exceptions."""


class LinkDingCliError(Exception):
    """Define a base exception."""

    pass


class ConfigError(LinkDingCliError):
    """Define an exception related to bad configuration."""

    pass
