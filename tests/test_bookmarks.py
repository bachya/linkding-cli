"""Define tests for the bookmark-related operations."""
import json
from unittest.mock import AsyncMock, patch

from aiolinkding.errors import LinkDingError
import pytest

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
            "website_title": "Website title",
            "website_description": "Website description",
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
    "website_title": "Website title",
    "website_description": "Website description",
    "tag_names": ["tag1", "tag2"],
    "date_added": "2020-09-26T09:46:23.006313Z",
    "date_modified": "2020-09-26T16:01:14.275335Z",
}


@pytest.mark.parametrize(
    "args,api_coro,api_coro_args,api_coro_kwargs,api_output,stdout_output",
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
            {"archived": False},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "-a"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"archived": True},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "-t", "Example"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"archived": False, "title": "Example"},
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
                "archived": False,
                "description": "A site description",
                "title": "Example",
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
                "archived": False,
                "description": "A site description",
                "tag_names": ["single-tag"],
                "title": "Example",
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
                "archived": False,
                "description": "A site description",
                "tag_names": ["tag1", "tag2", "tag3"],
                "title": "Example",
            },
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
            ["bookmarks", "update", "12", "-u", "https://example.com"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {"url": "https://example.com"},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "update", "12", "-t", "Updated Title"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {"title": "Updated Title"},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "update", "12", "--tags", "different-tag1,different-tag2"],
            "aiolinkding.bookmark.BookmarkManager.async_update",
            [12],
            {"tag_names": ["different-tag1", "different-tag2"]},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
    ],
)
def test_bookmark_command_api_calls(
    args, api_coro, api_coro_args, api_coro_kwargs, api_output, runner, stdout_output
):
    """Test various `linkding bookmarks` commands/API calls."""
    with patch(api_coro, AsyncMock(return_value=api_output)) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_with(*api_coro_args, **api_coro_kwargs)
    assert stdout_output in result.stdout


def test_update_no_options(caplog, runner):
    """Test that attempting to update a bookmark with no options fails."""
    runner.invoke(APP, ["bookmarks", "update", "12"])
    assert (
        "Cannot update a bookmark with passing at least one option."
        in caplog.messages[0]
    )
