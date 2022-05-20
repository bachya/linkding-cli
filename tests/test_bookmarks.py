"""Define tests for the bookmark-related operations."""
import json
from unittest.mock import AsyncMock, patch

import pytest

from linkding_cli.main import APP


def test_bookmarks_all(bookmarks_async_get_all_response, runner):
    """Test the `linkding bookmarks all` command."""
    with patch(
        "aiolinkding.bookmark.BookmarkManager.async_get_all",
        AsyncMock(return_value=bookmarks_async_get_all_response),
    ):
        result = runner.invoke(APP, ["bookmarks", "all"])

    bookmarks = json.loads(result.stdout.rstrip())
    assert len(bookmarks["results"]) == 1
    assert bookmarks["results"][0]["title"] == "Example title"
