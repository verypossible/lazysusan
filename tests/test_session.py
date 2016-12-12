import pytest

from datetime import (
    datetime,
    timedelta,
)
from lazysusan.session import Session


@pytest.fixture()
def session():
    return Session(user_id="testuser", session_key="THRIVE_STATE")


def test_get_backend_memory(session):
    assert session._backend.__class__.__name__ == "Memory"


def test_get_backend_dynamodb(mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_SESSION_STORAGE_BACKEND": "dynamodb"})
    session = Session(user_id="dynamodb", session_key="THRIVE_STATE")
    assert session._backend.__class__.__name__ == "DynamoDB"


def test_get_backend_cookie(mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_SESSION_STORAGE_BACKEND": "cookie"})
    session = Session(user_id="dynamodb", session_key="THRIVE_STATE", event={"session": {"attributes": {}}})
    assert session._backend.__class__.__name__ == "Memory"


def test_get_backend_cookie(mocker):
    event = {
        "session": {
            "attributes": {
                "THRIVE_STATE": "foobar"
            }
        }
    }
    mocker.patch.dict("os.environ", {"LAZYSUSAN_SESSION_STORAGE_BACKEND": "cookie"})
    session = Session(user_id="dynamodb", session_key="THRIVE_STATE", event=event)
    assert session.get_state() == "foobar"


def test_get_backend_cookie_bad_event(mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_SESSION_STORAGE_BACKEND": "cookie"})
    session = Session(user_id="dynamodb", session_key="THRIVE_STATE", event=("hi", "mom"))
    assert session._backend.__class__.__name__ == "Memory"


def test_get_backend_cookie_empty_event(mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_SESSION_STORAGE_BACKEND": "cookie"})
    session = Session(user_id="dynamodb", session_key="THRIVE_STATE", event={"session": {}})
    assert session._backend.__class__.__name__ == "Memory"


def test_get_state_default(session):
    assert session.get_state() == "initialState"


def test_get_state(session):
    session._backend["THRIVE_STATE"] = "foobar"
    assert session.get_state() == "foobar"


def test_get_audio_offset_default(session):
    assert session.get_audio_offset() == 0


def test_get_audio_offset_type_error(session):
    session._backend["AudioPlayer"] = None
    assert session.get_audio_offset() == 0


def test_get_audio_offset(session):
    session._backend["AudioPlayer"] = {"offsetInMilliseconds": 111}
    assert session.get_audio_offset() == 111


def test_update_audio_state(session):
    context = {"AudioPlayer": {"offsetInMilliseconds": 123}}
    session.update_audio_state(context)
    assert session._backend == context


def test_update_audio_state_context_key_error(session):
    assert session.update_audio_state({}) is None
    assert session._backend == {}


def test_update_audio_state_context_none(session):
    assert session.update_audio_state(None) is None
    assert session._backend == {}


def test_set_value(session):
    session.set("magickey", 12345)
    assert session._backend["magickey"] == 12345


def test_set_none(session):
    session.set("magickey", None)
    assert session._backend["magickey"] == None


def test_get_value(session):
    session._backend["magickey"] = "hello"
    assert session.get("magickey") == "hello"


def test_get_missing(session):
    assert session.get("magickey") is None


def test_get_missing_with_default(session):
    assert session.get("magickey", "default") == "default"


def test_set_request_time(session):
    ts = datetime(2016, 12, 8, 16, 38, 5, 0)
    session.last_request_time = ts
    assert session.last_request_time == ts


def test_default_last_request_time(session):
    assert isinstance(session.last_request_time, datetime)


def test_is_not_expired(session, mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_TTL_SECONDS": "100"})
    assert session.is_expired == False


def test_is_expired(session, mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_TTL_SECONDS": "100"})
    yesterday = datetime.now() - timedelta(days=1)
    session.last_request_time = yesterday
    assert session.is_expired == True


def test_is_expired_disabled(session, mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_TTL_SECONDS": "-1"})
    assert session.is_expired == False


def test_is_expired_bad(session, mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_TTL_SECONDS": "abc1"})
    with pytest.raises(ValueError):
        session.is_expired


def test_clear(session):
    session._backend["barney"] = "rubble"
    session.clear()
    assert session._backend["userId"] == "testuser"
