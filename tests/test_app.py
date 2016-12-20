import os
import pytest

from lazysusan.app import LazySusanApp


CWD = os.path.dirname(os.path.realpath(__file__))
EXPECTED_KEYS = ["outputSpeech", "shouldEndSession"]


@pytest.fixture
def app():
    return LazySusanApp(os.path.join(CWD, "states.yml"))


def assert_response(response, next_state, session, expected_response_keys=None):
    assert response
    assert session["LAZYSUSAN_STATE"] == next_state
    if expected_response_keys:
        assert sorted(response["response"].keys()) == sorted(expected_response_keys)


def test_launch_request(app, mock_session_backend, launch_request):
    response = app.handle(launch_request)
    assert_response(response, "invalidIntent", mock_session_backend, EXPECTED_KEYS)
