"""Define tests for the bookmark-related operations."""
import pytest

from src.main import APP


def test_bookmarks_all(runner):
    """Test the `linkding bookmarks all` command."""
    result = runner.invoke(APP, ["bookmarks", "all"])
    assert "PLACEHOLDER" in result.stdout
