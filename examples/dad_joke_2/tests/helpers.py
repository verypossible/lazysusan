import handler


class Chicken(object):
    keys = ["shouldEndSession", "outputSpeech", "card"]
    ends_session = True


class Dentist(object):
    keys = ["shouldEndSession", "outputSpeech", "card"]
    ends_session = True


class GoodBye(object):
    keys = ["shouldEndSession", "outputSpeech", "directives"]
    ends_session = True


class InitialState(object):
    keys = ["shouldEndSession", "outputSpeech", "card"]
    ends_session = False


class InvalidIntent(object):
    keys = ["outputSpeech", "shouldEndSession"]
    ends_session = True


class Lifesavers(object):
    keys = ["shouldEndSession", "outputSpeech", "card"]
    ends_session = True


STATE_TO_RESPONSE_WRAPPER = {
    "chicken": Chicken,
    "dentist": Dentist,
    "goodBye": GoodBye,
    "initialState": InitialState,
    "invalidIntent": InvalidIntent,
    "lifesavers": Lifesavers,
}


def assert_response(request, next_state, backend):
    response = handler.main(request, None)
    assert response["response"]

    assert backend["JOKES_STATE"] == next_state

    expected_response_wrapper = STATE_TO_RESPONSE_WRAPPER[next_state]

    assert sorted(response["response"].keys()) == sorted(expected_response_wrapper.keys)
    assert response["response"]["shouldEndSession"] == expected_response_wrapper.ends_session

    return response
