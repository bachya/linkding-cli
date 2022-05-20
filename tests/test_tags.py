"""Define tests for the tag-related operations."""
import pytest

from linkding_cli.main import APP


def test_tags_all(runner):
    """Test the `linkding tags all` command."""
    result = runner.invoke(APP, ["tags", "all"])
    assert "PLACEHOLDER" in result.stdout
