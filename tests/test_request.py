import pytest

from datetime import datetime
from lazysusan.request import Request


@pytest.fixture()
def alexa_request():
    return {
        "type": "IntentRequest",
        "requestId": "bob",
        "locale": "en-US",
        "timestamp": "2016-12-08T20:34:09Z",
        "intent": {
            "name": "GotAnIntent",
            "slots": {
                "WhatSlot": {
                    "name": "WhatSlot",
                    "value": "ThisSlot",
                    }
                }
            }
    }


@pytest.fixture()
def launch_request():
    return {
        "type": "LaunchRequest",
        "requestId": "bob",
        "locale": "en-US",
        "timestamp": "2016-12-08T20:34:09Z",
    }


def test_create_an_intent(alexa_request):
    new_request = Request(alexa_request)
    assert new_request._request == alexa_request


def test_raw_request(alexa_request):
    new_request = Request(alexa_request)
    assert new_request.raw == alexa_request


def test_request_timestamp(alexa_request):
    new_request = Request(alexa_request)
    assert new_request.timestamp == datetime(2016, 12, 8, 20, 34, 9)


def test_request_with_bad_intent_name():
    with pytest.raises(Exception):
        Request({}).intent_name


def test_request_type(alexa_request):
    new_request = Request(alexa_request)
    assert new_request.request_type == "IntentRequest"


def test_launch_request_type(launch_request):
    new_request = Request(launch_request)
    assert new_request.request_type == "LaunchRequest"


def test_get_slot_value(alexa_request):
    new_request = Request(alexa_request)
    assert new_request.get_slot_value("WhatSlot") == "ThisSlot"
