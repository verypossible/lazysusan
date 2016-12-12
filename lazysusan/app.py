import json
import os
import sys

import yaml

from constants import *
from logger import get_logger
from request import Request
from response import build_response_payload
from session import Session


_logger = get_logger()


def _load_state_machine(filename):
    with open(filename, 'r') as fh:
        return yaml.load(fh)



class LazySusanApp(object):

    def __init__(self, state_file, session_key="LAZYSUSAN_STATE"):
        self.__state_machine = _load_state_machine(state_file)
        self.__session_key = session_key


    @staticmethod
    def get_user_id_from_event(event):
        """
        Uncomment this if statement and populate with your skill's application ID to
        prevent someone else from configuring a skill that sends requests to this
        function.
        """
        # if (event["session"]["application"]["applicationId"] !=
        #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        #     raise ValueError("Invalid Application ID")

        # Note that session can be empty when we're playing long-form audio
        try:
            return event["session"]["user"]["userId"]
        except KeyError:
            pass

        try:
            return event["context"]["System"]["user"]["userId"]
        except KeyError:
            pass

        _logger.error(event)
        raise Exception("Could not find userId in lambda event")


    def build_response(self, request, session, intent_name, context, user_id):
        state = session.get_state()
        _logger.info("Current state: %s" % (state, ))

        # Determine what our response is by looking up our current state followed by
        # the intent_name in the request. Each state must define a "default" branch.
        branches = self.__state_machine[state]["branches"]

        try:
            branch = branches[intent_name]
        except KeyError:
            branch = branches["default"]

        # Allow us to specifically short-circuit and *not* return a request. This is due
        # to certain cases where a callback from Alexa does not accept any type of response. Typically
        # this is during audio playback for long-form audio.
        if branch is None:
            session.update_audio_state(context)
            return

        # now branch is the next state
        if callable(branch):
            branch_or_response = branch(request, session, intent_name, context, user_id,
                    self.__state_machine)
            if isinstance(branch_or_response, dict):
                return branch_or_response
            else:
                # not it's just a key
                branch = branch_or_response

        session.update_state(branch, context)

        branch = self.__state_machine[branch]
        response = branch["response"]

        if branch.get('get_audio_offset_from_session', False):
            offset = session.get_audio_offset()
            response['directives'][0]['audioItem']['stream']['offsetInMilliseconds'] = offset

        response_payload = build_response_payload(response, session.get_state_params())

        return response_payload


    def handle(self, event, lambda_context=None):
        """Main handler which receives initial request from Lambda.

        Route the incoming request based on type LaunchRequest, IntentRequest, etc.).

        :attr event: JSON payload which is sent from the Alexa service, containing relevant
                     info about the request
        :attr context: Lambda context
        """
        # Leave this in for logging
        _logger.info("Event: %s" % (event, ))

        request = Request(event["request"])
        context = event.get("context")

        user_id = LazySusanApp.get_user_id_from_event(event)

        session = Session(user_id, self.__session_key, event)
        if session.is_expired:
            session.clear()

        response = self.build_response(request, session, request.intent_name, context, user_id)

        session.save()

        # Leave this in for logging
        _logger.info("Response: %s" % (response, ))
        return response
