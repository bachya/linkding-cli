"""Define dynamic fixtures."""
from __future__ import annotations

import pytest
from typer.testing import CliRunner

from linkding_cli.const import ENV_TOKEN, ENV_URL

from .common import TEST_RAW_JSON, TEST_TOKEN, TEST_URL


@pytest.fixture(name="config", scope="session")
def config_fixture() -> str:
    """Define a fixture to return raw configuration data.

    Returns:
        A JSON string.
    """
    return TEST_RAW_JSON


@pytest.fixture(name="config_filepath")
def config_filepath_fixture(config: str, tmp_path: str) -> str:
    """Define a fixture to return a config filepath.

    Args:
        config: A JSON string.
        tmp_path: A basepath to save the config at.

    Returns:
        A full config filepath.
    """
    config_filepath = f"{tmp_path}/config.json"
    with open(config_filepath, "w", encoding="utf-8") as config_file:
        config_file.write(config)
    return config_filepath


@pytest.fixture(name="runner")
def runner_fixture() -> CliRunner:
    """Define a fixture to return a typer CLI test runner.

    Returns:
        A Typer CliRunner object.
    """
    return CliRunner(env={ENV_TOKEN: TEST_TOKEN, ENV_URL: TEST_URL})
