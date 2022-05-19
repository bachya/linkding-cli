"""Define common test utilities."""
import json
import os

from src.const import CONF_TOKEN, CONF_URL

TEST_TOKEN = "abcde_1234"
TEST_URL = "http://127.0.0.1:800"

TEST_RAW_JSON = json.dumps({CONF_TOKEN: TEST_TOKEN, CONF_URL: TEST_URL})
TEST_RAW_YAML = f"""
---
{CONF_TOKEN}: {TEST_TOKEN}
{CONF_URL}: {TEST_URL}
"""


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
