"""Define dynamic fixtures."""
import json

import pytest
from typer.testing import CliRunner

from linkding_cli.const import ENV_TOKEN, ENV_URL

from .common import TEST_RAW_JSON, TEST_TOKEN, TEST_URL, load_fixture


@pytest.fixture(name="bookmarks_async_get_all_response", scope="session")
def bookmarks_async_get_all_response_fixture():
    """Define a fixture to return all bookmarks."""
    return json.loads(load_fixture("bookmarks_async_get_all_response.json"))


@pytest.fixture(name="config", scope="session")
def config_fixture():
    """Define a fixture to return raw configuration data."""
    return TEST_RAW_JSON


@pytest.fixture(name="config_filepath")
def config_filepath_fixture(config, tmp_path):
    """Define a fixture to return a config filepath."""
    config_filepath = f"{tmp_path}/config.json"
    with open(config_filepath, "w", encoding="utf-8") as config_file:
        config_file.write(config)
    return config_filepath


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a typer CLI test runner."""
    return CliRunner(env={ENV_TOKEN: TEST_TOKEN, ENV_URL: TEST_URL})
