"""Define tests for the main CLI."""
import pytest
from typer.testing import CliRunner

from src.main import APP

RUNNER = CliRunner()


@pytest.mark.parametrize("args", [[], ["bookmarks"], ["tags"]])
def test_missing_command(args):
    """Test a missing command."""
    result = RUNNER.invoke(APP, [])
    assert result.exit_code == 2
    assert "Missing command" in result.stdout


def test_verbose_logging():
    """Test verbose logging."""
    result = RUNNER.invoke(APP, ["bookmarks"])
    assert not any(
        line for line in result.stdout.rstrip().split("\n") if "DEBUG" in line
    )

    result = RUNNER.invoke(APP, ["-v", "bookmarks"])
    assert any(line for line in result.stdout.rstrip().split("\n") if "DEBUG" in line)
