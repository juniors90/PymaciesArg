import os

import pytest


from sqlalchemy import create_engine


@pytest.fixture
def file_path():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    base = os.path.dirname(root_dir)
    _file_path = os.path.join(base, "tests")
    return _file_path


@pytest.fixture
def engine():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    base = os.path.dirname(root_dir)
    uri = "sqlite:///" + os.path.join(base, "tests", "test.db")
    _engine = create_engine(uri)
    return _engine
