"""Define tests for the bookmark-related operations."""
import pytest
from typer.testing import CliRunner

from src.main import APP

RUNNER = CliRunner()


def test_bookmarks_all():
    """Test the `linkding bookmarks all` command."""
    result = RUNNER.invoke(APP, ["bookmarks", "all"])
    assert "PLACEHOLDER" in result.stdout
