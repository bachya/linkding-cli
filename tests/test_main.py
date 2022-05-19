"""Define tests for the main CLI."""
import pytest
from typer.testing import CliRunner

from src.const import CONF_TOKEN, CONF_URL
from src.main import APP

from .common import TEST_TOKEN, TEST_URL


@pytest.mark.parametrize("args", [[], ["bookmarks"], ["tags"]])
def test_missing_command(args, runner):
    """Test a missing command."""
    result = runner.invoke(APP, [])
    assert result.exit_code == 2
    assert "Missing command" in result.stdout


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize(
    "args,missing_arg",
    [
        (["bookmarks"], CONF_TOKEN),
        (["-u", TEST_URL, "bookmarks"], CONF_TOKEN),
        (["-t", TEST_TOKEN, "bookmarks"], CONF_URL),
    ],
)
def test_missing_required_options(args, missing_arg, runner):
    """Test missing required options."""
    result = runner.invoke(APP, args)
    assert "Missing required option" in result.stdout
    for arg in missing_arg:
        assert arg in result.stdout


@pytest.mark.parametrize("runner", [CliRunner()])
def test_url_and_token_via_arguments(runner):
    """Test passing linkding URL and token via explicit CLI arguments."""
    result = runner.invoke(APP, ["-v", "-u", TEST_URL, "-t", TEST_TOKEN, "bookmarks"])
    [params] = [
        line
        for line in result.stdout.rstrip().split("\n")
        if "Starting CLI with parameters" in line
    ]
    assert f"'token': '{TEST_TOKEN}'" in params
    assert f"'url': '{TEST_URL}'" in params


def test_url_and_token_via_env_vars(runner):
    """Test passing linkding URL and token via environment variables."""
    result = runner.invoke(APP, ["-v", "bookmarks"])
    [params] = [
        line
        for line in result.stdout.rstrip().split("\n")
        if "Starting CLI with parameters" in line
    ]
    assert f"'token': '{TEST_TOKEN}'" in params
    assert f"'url': '{TEST_URL}'" in params


def test_verbose_logging(runner):
    """Test verbose logging."""
    result = runner.invoke(APP, ["bookmarks"])
    assert not any(
        line for line in result.stdout.rstrip().split("\n") if "DEBUG" in line
    )

    result = runner.invoke(APP, ["-v", "bookmarks"])
    assert any(line for line in result.stdout.rstrip().split("\n") if "DEBUG" in line)
