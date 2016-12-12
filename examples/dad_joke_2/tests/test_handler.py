import pytest

from callbacks import dad_joke


def _build_request_slot(name):
    return {
        "intent": {
            "slots": {
            }
        }
    }


def test_random_path():
    path_name = dad_joke(request=None, session=None)
    assert path_name
    assert path_name.endswith("Path")
