def get_slot_value(request, slot_name):
    try:
        return request["intent"]["slots"][slot_name]["value"]
    except KeyError:
        return None


def build_response(state_key, message, state_machine):
    response = state_machine[state_key]["response"]
    response["outputSpeech"]["text"] = message
    return response
