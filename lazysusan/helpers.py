def build_response(state_key, message, state_machine):
    response = state_machine[state_key]["response"]
    response["outputSpeech"]["text"] = message
    return response
