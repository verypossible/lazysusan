import pytest

from lazysusan import helpers


@pytest.fixture
def alexa_request():
    return {
        "intent": {
            "slots": {
                "foo": {
                    "name": "foo",
                    "value": "thevalue",
                }
            }
        }
    }

@pytest.fixture
def state_machine():
    return {
        "state_key": {
            "response": {
                "type": "PlainText",
                "outputSpeech": {
                    "text": "default text"
                }
            }
        }
    }


def test_get_slot_value(alexa_request):
    assert helpers.get_slot_value(alexa_request, "foo") == "thevalue"


def test_get_slot_value_missing(alexa_request):
    assert helpers.get_slot_value(alexa_request, "baz") is None


def test_get_slot_value_bad_request():
    alexa_request = {}
    assert helpers.get_slot_value(alexa_request, "foo") is None


def test_build_response(state_machine):
    expected = {"outputSpeech": {"text": "Hello world!"}, "type": "PlainText"}
    assert helpers.build_response("state_key", "Hello world!", state_machine) == expected


def test_build_response_key_error():
    with pytest.raises(KeyError):
        helpers.build_response("state_key", "Hello world!", {})
