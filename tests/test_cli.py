"""Define tests for configuration."""
import logging

import pytest
from typer.testing import CliRunner

from linkding_cli.cli import APP
from linkding_cli.const import CONF_TOKEN, CONF_URL, ENV_TOKEN
from linkding_cli.helpers.logging import TyperLoggerHandler

from .common import TEST_RAW_JSON, TEST_RAW_YAML, TEST_TOKEN, TEST_URL


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize("config", [TEST_RAW_JSON, TEST_RAW_YAML])
def test_config_file(caplog, config_filepath, runner):
    """Test successfully loading a valid config file."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath, "bookmarks"])
    assert (
        f"<Config token={TEST_TOKEN} url={TEST_URL} verbose=True>" in caplog.messages[3]
    )
    assert not any(
        level for _, level, _ in caplog.record_tuples if level == logging.ERROR
    )


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize("config", ["{}"])
def test_config_file_empty(caplog, config_filepath, runner):
    """Test an empty config file with no overrides."""
    runner.invoke(APP, ["-c", config_filepath, "bookmarks"])
    assert "Missing required option: --token" in caplog.messages[0]


@pytest.mark.parametrize("runner", [CliRunner()])
def test_config_file_overrides_cli(caplog, config_filepath, runner):
    """Test a config file with CLI option overrides."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath, "-t", "TEST_TOKEN", "bookmarks"])
    assert any(
        m
        for m in caplog.messages
        if f"<Config token=TEST_TOKEN url={TEST_URL} verbose=True>" in m
    )

    runner.invoke(APP, ["-v", "-c", config_filepath, "-u", "TEST_URL", "bookmarks"])
    assert any(
        m
        for m in caplog.messages
        if f"<Config token={TEST_TOKEN} url=TEST_URL verbose=True>" in m
    )


@pytest.mark.parametrize("runner", [CliRunner(env={ENV_TOKEN: "TEST_TOKEN"})])
def test_config_file_overrides_env_vars(caplog, config_filepath, runner):
    """Test a config file with environment variable overrides."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-c", config_filepath, "bookmarks"])
    assert (
        f"<Config token=TEST_TOKEN url={TEST_URL} verbose=True>" in caplog.messages[3]
    )


@pytest.mark.parametrize("runner", [CliRunner()])
@pytest.mark.parametrize("config", ["Fake configuration!"])
def test_config_file_unparsable(caplog, config_filepath, runner):
    """Test a config file that can't be parsed as JSON or YAML."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-c", config_filepath, "bookmarks"])
    assert "Unable to parse config file" in caplog.messages[3]


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
def test_missing_required_cli_options(args, caplog, missing_arg, runner):
    """Test missing required options when only using the CLI."""
    runner.invoke(APP, args)
    assert "Missing required option" in caplog.messages[0]
    for arg in missing_arg:
        assert arg in caplog.messages[0]


def test_startup_logging(caplog, runner):
    """Test startup logging at various levels."""
    caplog.set_level(logging.INFO)
    runner.invoke(APP, ["bookmarks"])
    info_log_messages = caplog.messages

    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "bookmarks"])
    debug_log_messages = caplog.messages

    # There should be more DEBUG-level logs than INFO-level logs:
    assert len(debug_log_messages) > len(info_log_messages)


def test_typer_logging_handler(caplog, runner):
    """Test the TyperLoggerHandler helper."""
    caplog.set_level(logging.DEBUG)

    handler = TyperLoggerHandler()
    logger = logging.getLogger("test")
    logger.addHandler(handler)

    logger.critical("Test Critical Message")
    logger.debug("Test Debug Message")
    logger.error("Test Error Message")
    logger.info("Test Info Message")
    logger.warning("Test Warning Message")

    assert len(caplog.messages) == 5


@pytest.mark.parametrize("runner", [CliRunner()])
def test_url_and_token_via_arguments(caplog, runner):
    """Test passing linkding URL and token via explicit CLI arguments."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "-u", TEST_URL, "-t", TEST_TOKEN, "bookmarks"])
    assert (
        f"<Config token={TEST_TOKEN} url={TEST_URL} verbose=True" in caplog.messages[3]
    )


def test_url_and_token_via_env_vars(caplog, runner):
    """Test passing linkding URL and token via environment variables."""
    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v", "bookmarks"])
    assert (
        f"<Config token={TEST_TOKEN} url={TEST_URL} verbose=True" in caplog.messages[3]
    )


@pytest.mark.parametrize(
    "args",
    [
        ["bookmarks"],
        ["bookmarks", "all"],
        ["tags", "all"],
    ],
)
def test_verbose_logging(args, caplog, runner):
    """Test verbose logging."""
    caplog.set_level(logging.INFO)
    runner.invoke(APP, args)
    info_log_messages = caplog.messages

    caplog.set_level(logging.DEBUG)
    runner.invoke(APP, ["-v"] + args)
    debug_log_messages = caplog.messages

    # There should be more DEBUG-level logs than INFO-level logs:
    assert len(debug_log_messages) > len(info_log_messages)
