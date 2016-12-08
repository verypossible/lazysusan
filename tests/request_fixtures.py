import pytest

from uuid import uuid4


USER_ID = "amzn1.ask.account.AHVPRU3PVMYSCNY"
APP_ID = "amzn1.ask.skill.{}".format(uuid4())


def build_request(request_type, request_intent=None, user_id=USER_ID):
    alexa_request = {
        "version": "1.0",
        "session": {
            "new": True,
            "sessionId": "amzn1.echo-api.session.{}".format(uuid4()),
            "user": {
                "userId": user_id,
            },
            "application": {
                "applicationId": APP_ID,
            }
        },
        "request": {
            "locale": "en-US",
            "timestamp": "2016-11-21T20:46:15Z",
            "type": request_type,
            "requestId": "amzn1.echo-api.request.{}".format(uuid4()),
        },
        "context": {
            "AudioPlayer": {
                "playerActivity": "STOPPED"
            },
            "System": {
                "device": {
                    "supportedInterfaces": {
                        "AudioPlayer": {}
                    }
                },
                "application": {
                    "applicationId": APP_ID,
                },
                "user": {
                    "userId": user_id,
                }
            }
        }
    }

    if request_intent:
        alexa_request["request"]["intent"] = request_intent

    return alexa_request


def build_audio_request(request_type, offset_in_ms=0, token="test", player_activity="PLAYING",
        user_id=USER_ID):
    assert request_type.startswith("AudioPlayer.")
    request = build_request(request_type, user_id=user_id)
    request.pop("session")
    request["request"].update({
        "offsetInMilliseconds": offset_in_ms,
        "token": token,
        "type": request_type,
    })
    request["context"]["AudioPlayer"].update({
        "token": token,
        "playerActivity": player_activity,
        "offsetInMilliseconds": offset_in_ms,
    })
    return request


def build_intent_request(intent_name, user_id=USER_ID):
    return build_request("IntentRequest", request_intent={"name": intent_name}, user_id=user_id)


@pytest.fixture()
def launch_request():
    return build_request("LaunchRequest")


@pytest.fixture()
def session_ended_request():
    alexa_request = build_request("SessionEndedRequest")
    alexa_request["reason"] = "EXCEEDED_MAX_REPROMPTS"
    return alexa_request


@pytest.fixture()
def cancel_intent():
    return build_intent_request("AMAZON.CancelIntent")


@pytest.fixture()
def help_intent():
    return build_intent_request("AMAZON.HelpIntent")


@pytest.fixture()
def pause_intent():
    return build_intent_request("AMAZON.PauseIntent")


@pytest.fixture()
def no_intent():
    return build_intent_request("AMAZON.NoIntent")


@pytest.fixture()
def start_over_intent():
    return build_intent_request("AMAZON.StartOverIntent")


@pytest.fixture()
def stop_intent():
    return build_intent_request("AMAZON.StopIntent")


@pytest.fixture()
def yes_intent():
    return build_intent_request("AMAZON.YesIntent")


@pytest.fixture()
def custom_intent():
    return build_intent_request("CustomIntent")


@pytest.fixture()
def dynamic_intent():
    return build_intent_request("DynamicIntent")


@pytest.fixture()
def audio_offset_intent():
    return build_intent_request("AudioOffsetIntent")


@pytest.fixture()
def playback_started_request():
    return build_audio_request("AudioPlayer.PlaybackStarted")


@pytest.fixture()
def playback_nearly_finished_request():
    return build_audio_request("AudioPlayer.PlaybackNearlyFinished", offset_in_ms=41000)


@pytest.fixture()
def playback_finished_request():
    return build_audio_request("AudioPlayer.PlaybackFinished", offset_in_ms=100000)


@pytest.fixture()
def resume_request():
    alexa_request = build_request("AMAZON.ResumeIntent")
    alexa_request["context"]["AudioPlayer"] = {
        "token": "meditation-token",
        "playerActivity": "STOPPED",
        "offsetInMilliseconds": 93888,
    }
    return alexa_request
