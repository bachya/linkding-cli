"""Define tests for the tag-related operations."""
import json
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from typer.testing import CliRunner

from linkding_cli.cli import APP

TAGS_ALL_RESPONSE = {
    "count": 123,
    "next": "http://127.0.0.1:8000/api/tags/?limit=100&offset=100",
    "previous": None,
    "results": [
        {
            "id": 1,
            "name": "example",
            "date_added": "2020-09-26T09:46:23.006313Z",
        }
    ],
}
TAGS_SINGLE_RESPONSE = {
    "id": 1,
    "name": "example-tag",
    "date_added": "2022-05-14T02:06:20.627370Z",
}


@pytest.mark.parametrize(
    "args,api_coro_path,api_coro_args,api_coro_kwargs,api_output,stdout_output",
    [
        (
            ["tags", "all"],
            "aiolinkding.tag.TagManager.async_get_all",
            [],
            {},
            TAGS_ALL_RESPONSE,
            json.dumps(TAGS_ALL_RESPONSE),
        ),
        (
            ["tags", "all", "-l", "10"],
            "aiolinkding.tag.TagManager.async_get_all",
            [],
            {"limit": 10},
            TAGS_ALL_RESPONSE,
            json.dumps(TAGS_ALL_RESPONSE),
        ),
        (
            ["tags", "all", "-o", "5"],
            "aiolinkding.tag.TagManager.async_get_all",
            [],
            {"offset": 5},
            TAGS_ALL_RESPONSE,
            json.dumps(TAGS_ALL_RESPONSE),
        ),
        (
            ["tags", "create", "sample-tag"],
            "aiolinkding.tag.TagManager.async_create",
            ["sample-tag"],
            {},
            TAGS_SINGLE_RESPONSE,
            json.dumps(TAGS_SINGLE_RESPONSE),
        ),
        (
            ["tags", "get", "12"],
            "aiolinkding.tag.TagManager.async_get_single",
            [12],
            {},
            TAGS_SINGLE_RESPONSE,
            json.dumps(TAGS_SINGLE_RESPONSE),
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
