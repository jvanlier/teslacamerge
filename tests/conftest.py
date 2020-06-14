from pathlib import Path

import pytest


@pytest.fixture
def fixture_path_abs():
    return Path(__file__).parent / "data"
