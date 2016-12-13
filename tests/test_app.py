import os
import pytest

from datetime import (
    datetime,
    timedelta,
)
from lazysusan.app import LazySusanApp

CWD = os.path.dirname(os.path.realpath(__file__))


def test_get_user_id_from_event_exception():
    with pytest.raises(Exception) as err:
        LazySusanApp.get_user_id_from_event({})

    assert str(err.value) == "Could not find userId in lambda event"


def test_get_user_id_from_session():
    event = {
        "session": {"user": {"userId": "brianz"}},
        "context": {"System": {"user": {"userId": "fooey"}}},
    }
    assert LazySusanApp.get_user_id_from_event(event) == "brianz"


def test_get_user_id_from_system():
    event = {
        "session": {"user": {"userIdNoWorkyWork": "brianz"}},
        "context": {"System": {"user": {"userId": "fooey"}}},
    }
    assert LazySusanApp.get_user_id_from_event(event) == "fooey"


@pytest.fixture
def app():
    return LazySusanApp(os.path.join(CWD, "states.yml"))


def assert_response(response, next_state, session, expected_response_keys=None):
    assert response
    assert session["LAZYSUSAN_STATE"] == next_state
    if expected_response_keys:
        assert sorted(response["response"].keys()) == sorted(expected_response_keys)


class TestInitialState(object):

    EXPECTED_KEYS = ["outputSpeech", "shouldEndSession"]

    def test_launch_request(self, app, mock_session_backend, launch_request):
        response = app.handle(launch_request)
        assert_response(response, "invalidIntent", mock_session_backend, self.EXPECTED_KEYS)

    def test_no_intent(self, app, mock_session_backend, no_intent):
        response = app.handle(no_intent)
        assert_response(response, "goodbyeIntent", mock_session_backend, self.EXPECTED_KEYS)

    def test_yes_intent(self, app, mock_session_backend, yes_intent):
        response = app.handle(yes_intent)
        expected_keys = self.EXPECTED_KEYS + ["card"]
        assert_response(response, "helloIntent", mock_session_backend, expected_keys)

    def test_custom_intent(self, app, mock_session_backend, custom_intent):
        response = app.handle(custom_intent)
        assert_response(response, "callbackIntent", mock_session_backend, self.EXPECTED_KEYS)

    def test_cancel_intent_no_state_change(self, app, mock_session_backend,
            playback_nearly_finished_request, get_state):
        get_state.return_value = "helloIntent"
        response = app.handle(playback_nearly_finished_request)

        expected_audio_state = {
            "playerActivity": "PLAYING",
            "token": "test",
            "offsetInMilliseconds": 41000,
        }
        assert "LAZYSUSAN_STATE" not in mock_session_backend
        assert sorted(response["response"].keys()) == sorted(self.EXPECTED_KEYS)
        assert mock_session_backend["AudioPlayer"] == expected_audio_state

    def test_dynamic_intent(self, app, mock_session_backend, dynamic_intent):
        response = app.handle(dynamic_intent)
        expected_msg = "this is some dynamic content"
        assert response["response"]["outputSpeech"]["text"] == expected_msg

    def test_audio_offset(self, app, mock_session_backend, audio_offset_intent, mocker):
        mock_get_offset = mocker.patch("lazysusan.session.Session.get_audio_offset")
        mock_get_offset.return_value = 111

        response = app.handle(audio_offset_intent)
        expected = {
            "audioItem": {
                "stream": {
                    "offsetInMilliseconds": 111
                }
            },
            "type": "AudioPlayer.Play"
        }
        assert response["response"]["directives"] == [expected]

    def test_playback_started(self, app, mock_session_backend, playback_started_request):
        response = app.handle(playback_started_request)
        assert response is None

    def test_playback_nearly_finished(self, app, mock_session_backend,
            playback_nearly_finished_request):
        response = app.handle(playback_nearly_finished_request)
        assert response is None

    def test_playback_finished(self, app, mock_session_backend, playback_finished_request):
        response = app.handle(playback_finished_request)
        assert response is None

    def test_session_cleared_and_saved(self, app, mock_session, launch_request):
        mock_session.is_expired = True
        mock_session.get_state.return_value = "initialState"

        response = app.handle(launch_request)
        assert mock_session.clear.call_count == 1
        assert mock_session.save.call_count == 1

    def test_session_last_request_time_is_set(self, app, mock_session_backend, launch_request):
        launch_request["request"]["timestamp"] = "2000-01-01T00:00:00Z"
        expected_dt = datetime(2000, 1, 1).isoformat()
        response = app.handle(launch_request)
        assert mock_session_backend["LAST_REQUEST_TIME"] == expected_dt
