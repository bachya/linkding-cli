"""Define utilities."""
from __future__ import annotations

from typing import Any


def generate_api_payload(param_pairs: tuple) -> dict[str, Any]:
    """Generate an aiolinkding payload dict from a set of param key/values.

    Args:
        param_pairs: A tuple of parameter key/value pairs.

    Returns:
        An API request payload.
    """
    payload = {}

    for key, value in param_pairs:
        if value is not None:
            payload[key] = value

    return payload
