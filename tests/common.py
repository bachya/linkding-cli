"""Define common test utilities."""
import json

from linkding_cli.const import CONF_TOKEN, CONF_URL, CONF_VERBOSE

TEST_TOKEN = "abcde_1234"
TEST_URL = "http://127.0.0.1:8080"

TEST_RAW_JSON = json.dumps(
    {
        CONF_TOKEN: TEST_TOKEN,
        CONF_URL: TEST_URL,
        CONF_VERBOSE: False,
    }
)
TEST_RAW_YAML = f"""
---
{CONF_TOKEN}: {TEST_TOKEN}
{CONF_URL}: {TEST_URL}
{CONF_VERBOSE}: false
"""
