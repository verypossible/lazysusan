import pytest

from uuid import uuid4


USER_ID = "amzn1.ask.account.AHVPRU3PVMYSCNY"
APP_ID = "amzn1.ask.skill.1e0ca6f4-473a-43eb-a8af-702c7f8728f3"


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


def build_intent_request(intent_name, user_id=USER_ID):
    return build_request("IntentRequest", request_intent={"name": intent_name}, user_id=user_id)


def build_jokes_launch_intent(path):
    return {
        "name": "JokesLaunchIntent",
        "slots": {
        }
    }


@pytest.fixture()
def LAUNCH_REQUEST():
    return build_request("LaunchRequest")


@pytest.fixture()
def SESSION_ENDED_REQUEST():
    alexa_request = build_request("SessionEndedRequest")
    alexa_request["reason"] = "EXCEEDED_MAX_REPROMPTS"
    return alexa_request


@pytest.fixture()
def CANCEL_INTENT():
    return build_intent_request("AMAZON.CancelIntent")


@pytest.fixture()
def HELP_INTENT():
    return build_intent_request("AMAZON.HelpIntent")


@pytest.fixture()
def PAUSE_INTENT():
    return build_intent_request("AMAZON.PauseIntent")


@pytest.fixture()
def NO_INTENT():
    return build_intent_request("AMAZON.NoIntent")


@pytest.fixture()
def START_OVER_INTENT():
    return build_intent_request("AMAZON.StartOverIntent")


@pytest.fixture()
def STOP_INTENT():
    return build_intent_request("AMAZON.StopIntent")


@pytest.fixture()
def YES_INTENT():
    return build_intent_request("AMAZON.YesIntent")


@pytest.fixture()
def JOKES_LAUNCH_INTENT():
    intent = build_jokes_launch_intent("")
    return build_request("IntentRequest", request_intent=intent)
