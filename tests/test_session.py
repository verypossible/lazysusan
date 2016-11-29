import pytest

from lazysusan.session import Session


@pytest.fixture()
def session():
    return Session(user_id="testuser", session_key="THRIVE_STATE")


def test_get_backend_memory(session):
    assert session._backend.__class__.__name__ == "Memory"


def test_get_backend_dynamodb(mocker):
    mocker.patch.dict("os.environ", {"LAZYSUSAN_STORAGE_BACKEND": "dynamodb"})
    session = Session(user_id="dynamodb", session_key="THRIVE_STATE")
    assert session._backend.__class__.__name__ == "DynamoDB"


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
