import yaml

from .logger import get_logger
from .request import Request
from .alexa_response import (
    build_empty_response,
    build_response,
    build_response_payload,
)
from .session import Session


_logger = get_logger()


def _load_state_machine(filename):
    with open(filename, "r") as fh:
        return yaml.load(fh)


class AlexaHandler(object):

    def __init__(self, state_file, session_key="LAZYSUSAN_STATE"):
        self.__state_machine = _load_state_machine(state_file)
        self.__session_key = session_key


    @staticmethod
    def get_user_id_from_event(event):
        """Lookup the userId in the request in multiple locations."""
        try:
            return event["session"]["user"]["userId"]
        except KeyError:
            # Note that session can be empty when we're playing long-form audio
            pass

        try:
            return event["context"]["System"]["user"]["userId"]
        except KeyError:
            pass

        _logger.error(event)
        raise Exception("Could not find userId in lambda event")


    def handle(self, event, lambda_context=None): #pylint: disable=locally-disabled,unused-argument
        """Main handler which receives initial request from Lambda.

        Route the incoming request based on type LaunchRequest, IntentRequest, etc.).

        :attr event: JSON payload which is sent from the Alexa service, containing relevant
                     info about the request
        :attr context: Lambda context
        """
        # Leave this in for logging
        _logger.info("Event: %s", event)

        request = Request(event["request"])
        context = event.get("context")

        user_id = AlexaHandler.get_user_id_from_event(event)

        session = Session(user_id, self.__session_key, event)
        if session.is_expired:
            session.clear()

        session.last_request_time = request.timestamp

        response = build_response(request, session, request.intent_name, context, user_id,
                self.__state_machine)

        session.save()

        # Leave this in for logging
        _logger.info("Response: %s", response)
        return response
