import pytest

from lazysusan import helpers


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



def test_build_response(state_machine):
    expected = {"outputSpeech": {"text": "Hello world!"}, "type": "PlainText"}
    assert helpers.build_response("state_key", "Hello world!", state_machine) == expected


def test_build_response_key_error():
    with pytest.raises(KeyError):
        helpers.build_response("state_key", "Hello world!", {})
