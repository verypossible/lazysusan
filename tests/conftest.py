import sys
import os

import pytest

from request_fixtures import *


os.environ["LAZYSUSAN_SESSION_STORAGE_BACKEND"] = "memory"
os.environ["LAZYSUSAN_SESSION_DYNAMODB_TABLE_NAME"] = "test"
os.environ["LAZYSUSAN_SESSION_AWS_REGION"] = "us-dummy-1"

CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(CWD)


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
def mock_session(mocker):
    mock_persistence = mocker.patch("lazysusan.persistence.Memory")
    backend = TestBackend()
    mock_persistence.return_value = backend
    return backend
