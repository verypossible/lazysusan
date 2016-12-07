from response import build_response_payload


def get_slot_value(request, slot_name):
    return request["intent"]["slots"][slot_name]["value"]


def build_dynamic_response(session, state_machine, dynamic_state_key, message):
    response = state_machine[dynamic_state_key]["response"]
    response["outputSpeech"]["test"] = message
    return build_response_payload(response, session.get_state_params())
