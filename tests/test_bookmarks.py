"""Define tests for the bookmark-related operations."""
from unittest.mock import AsyncMock, patch

from aiolinkding.errors import LinkDingError
import pytest

from linkding_cli.main import APP


@pytest.mark.parametrize(
    "args,api_coro,api_coro_args,api_coro_kwargs",
    [
        (
            ["bookmarks", "create", "https://example.com"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {},
        ),
        (
            ["bookmarks", "create", "https://example.com", "-t", "Example"],
            "aiolinkding.bookmark.BookmarkManager.async_create",
            ["https://example.com"],
            {"title": "Example"},
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
        ),
        (
            ["bookmarks", "all"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {},
        ),
        (
            ["bookmarks", "all", "--archived"],
            "aiolinkding.bookmark.BookmarkManager.async_get_archived",
            [],
            {},
        ),
        (
            ["bookmarks", "all", "--query", "test"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
            [],
            {"query": "test"},
        ),
        (
            ["bookmarks", "get", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_get_single",
            [12],
            {},
        ),
    ],
)
@pytest.mark.parametrize(
    "result,output",
    [
        (AsyncMock(side_effect=LinkDingError), "Error"),
        (AsyncMock(return_value="{}"), "{}"),
    ],
)
def test_bookmark_commands(
    args, api_coro, api_coro_args, api_coro_kwargs, output, result, runner
):
    """Test various `linkding bookmarks` commands (success and error)."""
    with patch(api_coro, result) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_with(*api_coro_args, **api_coro_kwargs)
    assert output in result.stdout
