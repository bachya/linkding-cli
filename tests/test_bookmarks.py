"""Define tests for the bookmark-related operations."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from typer.testing import CliRunner

from linkding_cli.cli import APP

BOOKMARKS_ALL_RESPONSE = {
    "count": 123,
    "next": "http://127.0.0.1:8000/api/bookmarks/?limit=100&offset=100",
    "previous": None,
    "results": [
        {
            "id": 1,
            "url": "https://example.com",
            "title": "Example title",
            "description": "Example description",
            "notes": "Example notes",
            "website_title": "Website title",
            "website_description": "Website description",
            "is_archived": False,
            "unread": False,
            "shared": False,
            "tag_names": ["tag1", "tag2"],
            "date_added": "2020-09-26T09:46:23.006313Z",
            "date_modified": "2020-09-26T16:01:14.275335Z",
        }
    ],
}
BOOKMARKS_SINGLE_RESPONSE = {
    "id": 1,
    "url": "https://example.com",
    "title": "Example title",
    "description": "Example description",
    "notes": "Example notes",
    "website_title": "Website title",
    "website_description": "Website description",
    "is_archived": False,
    "unread": False,
    "shared": False,
    "tag_names": ["tag1", "tag2"],
    "date_added": "2020-09-26T09:46:23.006313Z",
    "date_modified": "2020-09-26T16:01:14.275335Z",
}


@pytest.mark.parametrize(
    "args,api_coro_path,api_coro_args,api_coro_kwargs,api_output,stdout_output",
    [
        (
            ["bookmarks", "all"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {},
            BOOKMARKS_ALL_RESPONSE,
            json.dumps(BOOKMARKS_ALL_RESPONSE),
        ),
        (
            ["bookmarks", "all", "--archived"],
            "aiolinkding.bookmark.BookmarkManager.async_get_archived",
            [],
            {},
            BOOKMARKS_ALL_RESPONSE,
            json.dumps(BOOKMARKS_ALL_RESPONSE),
        ),
        (
            ["bookmarks", "all", "-l", "10"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {"limit": 10},
            BOOKMARKS_ALL_RESPONSE,
            json.dumps(BOOKMARKS_ALL_RESPONSE),
        ),
        (
            ["bookmarks", "all", "-o", "5"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {"offset": 5},
            BOOKMARKS_ALL_RESPONSE,
            json.dumps(BOOKMARKS_ALL_RESPONSE),
        ),
        (
            ["bookmarks", "all", "-q", "Example"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {"query": "Example"},
            BOOKMARKS_ALL_RESPONSE,
            json.dumps(BOOKMARKS_ALL_RESPONSE),
        ),
        (
            ["bookmarks", "archive", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_archive",
            [12],
            {},
            None,
            "Bookmark 12 archived.",
        ),
        (
            ["bookmarks", "create", "https://example.com"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"is_archived": False, "unread": False, "shared": False},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "-a", "--shared"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"is_archived": True, "unread": False, "shared": True},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "-n", "Example notes"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {
                "is_archived": False,
                "unread": False,
                "shared": False,
                "notes": "Example notes",
            },
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "-t", "Example"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {
                "is_archived": False,
                "title": "Example",
                "unread": False,
                "shared": False,
            },
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            [
                "bookmarks",
                "create",
                "https://example.com",
                "-t",
                "Example",
                "-d",
                "A site description",
            ],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {
                "description": "A site description",
                "is_archived": False,
                "shared": False,
                "title": "Example",
                "unread": False,
            },
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            [
                "bookmarks",
                "create",
                "https://example.com",
                "-t",
                "Example",
                "-d",
                "A site description",
                "--tags",
                "single-tag",
            ],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {
                "description": "A site description",
                "is_archived": False,
                "shared": False,
                "tag_names": ["single-tag"],
                "title": "Example",
                "unread": False,
            },
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            [
                "bookmarks",
                "create",
                "https://example.com",
                "-t",
                "Example",
                "-d",
                "A site description",
                "--tags",
                "tag1,tag2,tag3",
            ],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {
                "description": "A site description",
                "is_archived": False,
                "shared": False,
                "tag_names": ["tag1", "tag2", "tag3"],
                "title": "Example",
                "unread": False,
            },
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "--unread"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"is_archived": False, "unread": True, "shared": False},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "delete", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_delete",
            [12],
            {},
            None,
            "Bookmark 12 deleted.",
        ),
        (
            ["bookmarks", "get", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_get_single",
            [12],
            {},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "unarchive", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_unarchive",
            [12],
            {},
            None,
            "Bookmark 12 unarchived.",
        ),
        (
            ["bookmarks", "update", "12", "-u", "https://example.com", "--shared"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {"url": "https://example.com", "unread": False, "shared": True},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "update", "12", "-t", "Updated Title"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {"title": "Updated Title", "unread": False, "shared": False},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "update", "12", "--tags", "different-tag1,different-tag2"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {
                "tag_names": ["different-tag1", "different-tag2"],
                "unread": False,
                "shared": False,
            },
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "update", "12", "--unread"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {"unread": True, "shared": False},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
    ],
)
def test_bookmark_command_api_calls(
    args: list[str],
    api_coro_path: str,
    api_coro_args: list[int | str],
    api_coro_kwargs: dict[str, Any],
    api_output: dict[str, Any],
    runner: CliRunner,
    stdout_output: str,
) -> None:
    """Test various `linkding bookmarks` commands/API calls.

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
