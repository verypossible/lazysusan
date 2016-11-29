import pytest

from lazysusan.app import LazySusanApp


def test_get_intent_from_request_exception():
    with pytest.raises(Exception) as err:
        LazySusanApp.get_intent_from_request({})

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
