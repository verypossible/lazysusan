from lazysusan.helpers import build_response
from lazysusan.response import build_response_payload


def do_callback(request, session, intent, context, users_id, state_machine):
    return "callbackIntent"


def do_dynamic_callback(request, session, intent, context, users_id, state_machine):
    msg = "this is some dynamic content"
    response_dict = build_response("goodbyeIntent", msg, state_machine)
    return build_response_payload(response_dict, session.get_state_params())
