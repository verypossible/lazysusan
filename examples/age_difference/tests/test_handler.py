import pytest

from callbacks import calc_difference


def _build_request_slot(name):
    return {
        "intent": {
            "slots": {
            }
        }
    }


def test_calc():
    path_name = calc_difference(None, None, None, None, None, None)
    assert path_name
    assert path_name == "goodBye"
