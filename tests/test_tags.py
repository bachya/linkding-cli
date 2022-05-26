"""Define tests for the tag-related operations."""
import json
import logging
from unittest.mock import AsyncMock, patch

from aiolinkding.errors import LinkDingError
import pytest

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
    "args,api_coro,api_coro_args,api_coro_kwargs,api_output,stdout_output",
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
    args,
    api_coro,
    api_coro_args,
    api_coro_kwargs,
    api_output,
    caplog,
    runner,
    stdout_output,
):
    """Test various `linkding tags` commands/API calls."""
    with patch(api_coro, AsyncMock(return_value=api_output)) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_with(*api_coro_args, **api_coro_kwargs)
    assert stdout_output in result.stdout
