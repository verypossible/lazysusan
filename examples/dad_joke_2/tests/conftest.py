import sys
import os

import pytest

from request_fixtures import *

here = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(here, "../Jokes2"))

os.environ["LAZYSUSAN_SESSION_STORAGE_BACKEND"] = "memory"
os.environ["LAZYSUSAN_SESSION_DYNAMODB_TABLE_NAME"] = "test"
os.environ["LAZYSUSAN_SESSION_AWS_REGION"] = "us-dummy-1"


class TestBackend(dict):
    def connect(self, **kwargs):
        pass

    def save(self):
        pass


def pytest_configure(config):
    """Called at the start of the entire test run"""
    pass


@pytest.fixture(autouse=True)
def boto3(mocker):
    return mocker.patch("lazysusan.persistence.boto3")


@pytest.fixture()
def get_state(mocker):
    return mocker.patch("lazysusan.session.Session.get_state")


@pytest.fixture()
def initial_state(get_state):
    get_state.return_value = "initialState"
    return get_state


@pytest.fixture()
def mock_session(mocker):
    mock_persistence = mocker.patch("lazysusan.persistence.Memory")
    backend = TestBackend()
    mock_persistence.return_value = backend
    return backend
