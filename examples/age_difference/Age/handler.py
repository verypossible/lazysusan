from __future__ import print_function

import os
import sys

# Add in our lib/ directory so we can import extra packages
CWD = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CWD, "lib"))

import yaml

os.environ["LAZYSUSAN_SESSION_STORAGE_BACKEND"] = "cookie"
os.environ["LAZYSUSAN_LOG_LEVEL"] = "logging.INFO"
from lazysusan import LazySusanApp


def main(event, lambda_context):
    """Main handler which receives initial request from Lambda.

    Route the incoming request based on type LaunchRequest, IntentRequest, etc.).

    :attr event: JSON payload which is sent from the Alexa service, containing relevant
                 info about the request
    :attr context: Lambda context
    """
    state_path = os.path.join(CWD, "states.yml")
    app = LazySusanApp(state_path, session_key="AGE_STATE")
    response = app.handle(event)
    return response
