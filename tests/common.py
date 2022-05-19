"""Define common test utilities."""
import os

TEST_TOKEN = "abcde_1234"
TEST_URL = "http://127.0.0.1:800"


def load_fixture(filename):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
