"""Define dynamic fixtures."""
import pytest
from typer.testing import CliRunner

from src.const import ENV_TOKEN, ENV_URL

from .common import TEST_TOKEN, TEST_URL


@pytest.fixture(name="runner")
def runner_fixture():
    """Define a fixture to return a typer CLI test runner."""
    return CliRunner(env={ENV_TOKEN: TEST_TOKEN, ENV_URL: TEST_URL})
