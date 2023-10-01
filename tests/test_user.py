"""Define tests for the user-related operations."""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from typer.testing import CliRunner

from linkding_cli.cli import APP

USER_PROFILE_RESPONSE = {
    "theme": "auto",
    "bookmark_date_display": "relative",
    "bookmark_link_target": "_blank",
    "web_archive_integration": "enabled",
    "tag_search": "lax",
    "enable_sharing": True,
    "enable_public_sharing": True,
    "enable_favicons": False,
    "display_url": False,
    "permanent_notes": False,
    "search_preferences": {"sort": "title_asc", "shared": "off", "unread": "off"},
}


@pytest.mark.parametrize(
    "args,api_coro_path,api_coro_args,api_coro_kwargs,api_output,stdout_output",
    [
        (
            ["user", "profile"],
            "aiolinkding.user.UserManager.async_get_profile",
            [],
            {},
            USER_PROFILE_RESPONSE,
            json.dumps(USER_PROFILE_RESPONSE),
        ),
    ],
)
def test_tag_command_api_calls(
    args: list[str],
    api_coro_path: str,
    api_coro_args: list[int | str],
    api_coro_kwargs: dict[str, Any],
    api_output: dict[str, Any],
    runner: CliRunner,
    stdout_output: str,
) -> None:
    """Test various `linkding tags` commands/API calls.

    Args:
        args: The arguments to pass to the command.
        api_coro_path: The module path to a coroutine function.
        api_coro_args: The arguments to pass to the coroutine function.
        api_coro_kwargs: The keyword arguments to pass to the coroutine function.
        api_output: An API response payload.
        runner: A Typer CliRunner object.
        stdout_output: The output displayed on stdout.
    """
    with patch(api_coro_path, AsyncMock(return_value=api_output)) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_with(*api_coro_args, **api_coro_kwargs)
    assert stdout_output in result.stdout
