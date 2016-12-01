def build_response_payload(speechlet_response, state):
    """Build a valid Alexa response given a speechlet data structure.

    :attr speechlet_response: A data structure which conforms to the Alexa response type
    :type speechlet_response: dict

    """
    return {
        "version": "2.0",
        "sessionAttributes": state,
        "response": speechlet_response,
    }
