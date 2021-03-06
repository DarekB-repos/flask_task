import os
import sys
import inspect
import pytest
from bankApp import app

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


@pytest.fixture
def mock_admin_name() -> str:
    return "Admin"


def test_admin_name(mock_admin_name) -> None:
    assert mock_admin_name == "Admin"


def test_app():
    print(type(app))
