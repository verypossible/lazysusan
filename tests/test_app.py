import os
import pytest

from lazysusan.app import LazySusanApp

CWD = os.path.dirname(os.path.realpath(__file__))


def test_get_intent_name_from_request_exception():
    with pytest.raises(Exception) as err:
        LazySusanApp.get_intent_name_from_request({})

    assert "Could not find appropriate callback for intent" in str(err.value)


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

    def test_launch_request(self, app, mock_session, launch_request):
        response = app.handle(launch_request)
        assert_response(response, "invalidIntent", mock_session, self.EXPECTED_KEYS)

    def test_no_intent(self, app, mock_session, no_intent):
        response = app.handle(no_intent)
        assert_response(response, "goodbyeIntent", mock_session, self.EXPECTED_KEYS)

    def test_yes_intent(self, app, mock_session, yes_intent):
        response = app.handle(yes_intent)
        expected_keys = self.EXPECTED_KEYS + ["card"]
        assert_response(response, "helloIntent", mock_session, expected_keys)

    def test_custom_intent(self, app, mock_session, custom_intent):
        response = app.handle(custom_intent)
        assert_response(response, "callbackIntent", mock_session, self.EXPECTED_KEYS)

    def test_dynamic_intent(self, app, mock_session, dynamic_intent):
        response = app.handle(dynamic_intent)
        expected_msg = "this is some dynamic content"
        assert response["response"]["outputSpeech"]["text"] == expected_msg

    def test_audio_offset(self, app, mock_session, audio_offset_intent, mocker):
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

    def test_playback_started(self, app, mock_session, playback_started_request):
        response = app.handle(playback_started_request)
        assert response is None

    def test_playback_nearly_finished(self, app, mock_session, playback_nearly_finished_request):
        response = app.handle(playback_nearly_finished_request)
        assert response is None

    def test_playback_finished(self, app, mock_session, playback_finished_request):
        response = app.handle(playback_finished_request)
        assert response is None
