import os
import sys
import inspect
import pytest
import tempfile
from bankApp import app

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

app.testing=True
client=app.test_client()


def test_admin_name(mock_admin_name) -> None:
    assert mock_admin_name == "Admin"


def test_app():
    res=client.get("/")
    assert 'You should be redirected'