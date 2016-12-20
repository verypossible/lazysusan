from .logger import get_logger
from .alexa_handler import AlexaHandler

_logger = get_logger()


class LazySusanApp(object):

    def __init__(self, state_file, session_key="LAZYSUSAN_STATE"):
        self.__state_file = state_file
        self.__session_key = session_key


    def handle(self, event, lambda_context=None): #pylint: disable=locally-disabled,unused-argument
        """Main handler which receives initial request from Lambda.

        Route the incoming request based on type LaunchRequest, IntentRequest, etc.).

        :attr event: JSON payload which is sent from the Alexa service, containing relevant
                     info about the request
        :attr context: Lambda context
        """
        # Leave this in for logging

        # Handle Alexa Request
        _logger.info("Handle Alexa Request")
        request = AlexaHandler(self.__state_file, self.__session_key)
        response = request.handle(event, lambda_context)

        _logger.info("Alexa Response: %s", response)
        return response
