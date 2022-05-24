"""Define tests for the bookmark-related operations."""
import json
from unittest.mock import AsyncMock, patch

from aiolinkding.errors import LinkDingError
import pytest

from linkding_cli.main import APP

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
            ["bookmarks", "all", "--query", "Example"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {"query": "Example"},
            BOOKMARKS_ALL_RESPONSE,
            json.dumps(BOOKMARKS_ALL_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {},
            BOOKMARKS_SINGLE_RESPONSE,
            json.dumps(BOOKMARKS_SINGLE_RESPONSE),
        ),
        (
            ["bookmarks", "create", "https://example.com", "-t", "Example"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"title": "Example"},
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
            {"title": "Example", "description": "A site description"},
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
                "title": "Example",
                "description": "A site description",
                "tag_names": ["single-tag"],
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
                "title": "Example",
                "description": "A site description",
                "tag_names": ["tag1", "tag2", "tag3"],
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
    ],
)
def test_bookmark_commands(
    args, api_coro, api_coro_args, api_coro_kwargs, api_output, runner, stdout_output
):
    """Test various `linkding bookmarks` commands (success and error)."""
    with patch(api_coro, AsyncMock(return_value=api_output)) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_with(*api_coro_args, **api_coro_kwargs)
    assert stdout_output in result.stdout

    with patch(api_coro, AsyncMock(side_effect=LinkDingError)) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_with(*api_coro_args, **api_coro_kwargs)
    assert "Error" in result.stdout
