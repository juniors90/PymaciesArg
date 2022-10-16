import datetime
import os
import pathlib

from pymacies_arg import PymaciesArg

import pytest

from sqlalchemy import create_engine


now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day
date = f"{year}-{month}-{day}"

# this path is pointing to project/docs/source
CURRENT_PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))


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


@pytest.fixture
def pymacies():
    pymacies_obj = PymaciesArg(date, CURRENT_PATH)
    return pymacies_obj


@pytest.fixture
def date_str():
    return date
