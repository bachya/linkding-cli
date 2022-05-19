"""Define a data object."""
from __future__ import annotations

from typing import Any

from .config import Config


class LinkDing:
    """Define a master linkding manager object."""

    def __init__(self, params: dict[str, Any]) -> None:
        """Initialize."""
        self.config = Config(params)
