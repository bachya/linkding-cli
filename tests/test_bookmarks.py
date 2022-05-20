"""Define tests for the bookmark-related operations."""
from unittest.mock import AsyncMock, patch

from aiolinkding.errors import LinkDingError
import pytest

from linkding_cli.main import APP


@pytest.mark.parametrize(
    "args,patched_api_coro",
    [
        (
            ["bookmarks", "all"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
        ),
        (
            ["bookmarks", "all", "--archived"],
            "aiolinkding.bookmark.BookmarkManager.async_get_archived",
        ),
        (
            ["bookmarks", "all", "--query", "test"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
        ),
        (
            ["bookmarks", "id", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_get_single",
        ),
    ],
)
def test_bookmark_commands(args, patched_api_coro, runner):
    """Test various `linkding bookmarks` commands."""
    with patch(patched_api_coro, AsyncMock(return_value="output")) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_once()
    assert "output" in result.stdout


@pytest.mark.parametrize(
    "args,patched_api_coro",
    [
        (
            ["bookmarks", "all"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
        ),
        (
            ["bookmarks", "all", "--archived"],
            "aiolinkding.bookmark.BookmarkManager.async_get_archived",
        ),
        (
            ["bookmarks", "all", "--query", "test"],
            "aiolinkding.bookmark.BookmarkManager.async_get_all",
        ),
        (
            ["bookmarks", "id", "12"],
            "aiolinkding.bookmark.BookmarkManager.async_get_single",
        ),
    ],
)
def test_bookmark_errors(args, patched_api_coro, runner):
    """Test errors during various `linkding bookmarks` commands."""
    with patch(
        patched_api_coro, AsyncMock(side_effect=LinkDingError)
    ) as mocked_api_call:
        result = runner.invoke(APP, args)
        mocked_api_call.assert_awaited_once()
    assert "Error" in result.stdout
