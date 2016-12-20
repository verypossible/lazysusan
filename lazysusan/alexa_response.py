from .logger import get_logger

_logger = get_logger()


def build_empty_response():
    return build_response_payload({"shouldEndSession": True}, {})


def build_response(request, session, intent_name, context, user_id, state_machine):
    state = session.get_state()
    _logger.info("Current state: %s", state)

    # Determine what our response is by looking up our current state followed by
    # the intent_name in the request. Each state must define a "default" branch.
    branches = state_machine[state]["branches"]

    try:
        branch_name = branches[intent_name]
    except KeyError:
        branch_name = branches["default"]

    # Allow us to specifically short-circuit and *not* return a request. This is due to
    # certain cases where a callback from Alexa does not accept any type of response. Typically
    # this is during audio playback for long-form audio.
    if branch_name is None:
        session.update_audio_state(context)
        # For states where alexa does not want a response, we need to exit without returning
        # anything to prevent an Alexa platform error. As of this time, this has not been
        # documented clearly by Amazon.
        return build_empty_response()

    # now branch_name is the next state
    if callable(branch_name):
        branch_name_or_response = branch_name(
            request=request,
            session=session,
            intent_name=intent_name,
            context=context,
            user_id=user_id,
            state_machine=state_machine
        )
        if isinstance(branch_name_or_response, dict):
            return branch_name_or_response

        # now it's just a key
        branch_name = branch_name_or_response

    branch = state_machine[branch_name]

    if branch.get("is_state", True):
        session.update_state(branch_name)
    session.update_audio_state(context)

    response = branch["response"]

    if branch.get("get_audio_offset_from_session", False):
        offset = session.get_audio_offset()
        response["directives"][0]["audioItem"]["stream"]["offsetInMilliseconds"] = offset

    response_payload = build_response_payload(response, session.get_state_params())

    return response_payload


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
