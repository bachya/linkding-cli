"""Define package constants."""
import logging

LOGGER = logging.getLogger(__package__)

CONF_LIMIT = "limit"
CONF_OFFSET = "offset"
CONF_TOKEN = "token"  # noqa: S105, # nosec
CONF_URL = "url"
CONF_VERBOSE = "verbose"

ENV_CONFIG = "LINKDING_CONFIG"
ENV_TOKEN = "LINKDING_TOKEN"  # noqa: S105, # nosec
ENV_URL = "LINKDING_URL"
