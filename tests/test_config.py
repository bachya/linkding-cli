"""Define tests for configuration."""
import pytest
from typer.testing import CliRunner

from linkding_cli.const import CONF_TOKEN, CONF_URL, ENV_TOKEN
from linkding_cli.main import APP

from .common import TEST_RAW_JSON, TEST_RAW_YAML, TEST_TOKEN, TEST_URL


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize("config", [TEST_RAW_JSON, TEST_RAW_YAML])
def test_config_file(config_filepath, runner):
    """Test successfully loading a valid config file."""
    result = runner.invoke(APP, ["-v", "-c", config_filepath, "bookmarks"])
    assert f"<Config token={TEST_TOKEN} url={TEST_URL} verbose=True>" in result.stdout


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize("config", ["{}"])
def test_config_file_empty(config_filepath, runner):
    """Test an empty config file with no overrides."""
    result = runner.invoke(APP, ["-c", config_filepath, "bookmarks"])
    assert "Missing required option: --token" in result.stdout


@pytest.mark.parametrize("runner", [CliRunner()])
def test_config_file_overrides_cli(config_filepath, runner):
    """Test a config file with CLI option overrides."""
    result = runner.invoke(
        APP, ["-v", "-c", config_filepath, "-t", "TEST_TOKEN", "bookmarks"]
    )
    assert f"<Config token=TEST_TOKEN url={TEST_URL} verbose=True>" in result.stdout

    result = runner.invoke(
        APP, ["-v", "-c", config_filepath, "-u", "TEST_URL", "bookmarks"]
    )
    assert f"<Config token={TEST_TOKEN} url=TEST_URL verbose=True>" in result.stdout


@pytest.mark.parametrize("runner", [CliRunner(env={ENV_TOKEN: "TEST_TOKEN"})])
def test_config_file_overrides_env_vars(config_filepath, runner):
    """Test a config file with environment variable overrides."""
    result = runner.invoke(APP, ["-v", "-c", config_filepath, "bookmarks"])
    assert f"<Config token=TEST_TOKEN url={TEST_URL} verbose=True>" in result.stdout


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize("config", ["Fake configuration!"])
def test_config_file_unparsable(config_filepath, runner):
    """Test a config file that can't be parsed as JSON or YAML."""
    result = runner.invoke(APP, ["-c", config_filepath, "bookmarks"])
    assert "Unable to parse config file" in result.stdout


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
def test_missing_required_cli_options(args, missing_arg, runner):
    """Test missing required options when only using the CLI."""
    result = runner.invoke(APP, args)
    assert "Missing required option" in result.stdout
    for arg in missing_arg:
        assert arg in result.stdout


@pytest.mark.parametrize("runner", [CliRunner()])
def test_url_and_token_via_arguments(runner):
    """Test passing linkding URL and token via explicit CLI arguments."""
    result = runner.invoke(APP, ["-v", "-u", TEST_URL, "-t", TEST_TOKEN, "bookmarks"])
    assert f"<Config token={TEST_TOKEN} url={TEST_URL} verbose=True" in result.stdout


def test_url_and_token_via_env_vars(runner):
    """Test passing linkding URL and token via environment variables."""
    result = runner.invoke(APP, ["-v", "bookmarks"])
    assert f"<Config token={TEST_TOKEN} url={TEST_URL} verbose=True" in result.stdout


def test_verbose_logging(runner):
    """Test verbose logging."""
    result = runner.invoke(APP, ["bookmarks"])
    assert not any(
        line for line in result.stdout.rstrip().split("\n") if "Debug" in line
    )

    result = runner.invoke(APP, ["-v", "bookmarks"])
    assert any(line for line in result.stdout.rstrip().split("\n") if "Debug" in line)
