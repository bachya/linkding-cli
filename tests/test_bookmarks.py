"""Define tests for the bookmark-related operations."""
import json
from unittest.mock import AsyncMock, patch

import pytest

from linkding_cli.main import APP


@pytest.mark.parametrize(
    "args,patched_coro",
    [
        (["bookmarks", "all"], "aiolinkding.bookmark.BookmarkManager.async_get_all"),
        (
            ["bookmarks", "all", "--archived"],
            "aiolinkding.bookmark.BookmarkManager.async_get_archived",
        ),
    ],
)
def test_bookmarks_all(args, bookmarks_multiple, patched_coro, runner):
    """Test the `linkding bookmarks all` command."""
    with patch(patched_coro, AsyncMock(return_value=bookmarks_multiple)):
        result = runner.invoke(APP, args)

    bookmarks = json.loads(result.stdout.rstrip())
    assert len(bookmarks["results"]) == 1
    assert bookmarks["results"][0]["title"] == "Example title"
