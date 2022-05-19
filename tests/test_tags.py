"""Define tests for the tag-related operations."""
import pytest
from typer.testing import CliRunner

from src.main import APP

RUNNER = CliRunner()


def test_bookmarks_all():
    """Test the `linkding tags all` command."""
    result = RUNNER.invoke(APP, ["tags", "all"])
    assert "PLACEHOLDER" in result.stdout
