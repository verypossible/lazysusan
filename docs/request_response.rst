.. _request_response:

============================
Request/response cycle
============================

- Look at the current state
- Grab the matching yaml block for the current state
- Look at the Intent sent in the request
- Find the matching Intent in the ``branches`` map
- Reply with the response for that matching branch or ``default`` if the Intent isn't defined in
  the ``branches`` map

Example Request/Response Cycle
==============================

In order to explain the request/response cycle, consider the following
interation for the remainder of this tutorial:

::

    user: Alexa, ask recipe helper how to make scrambled eggs
    Alexa: Welcome to simple recipe helper. Would you like to make some scrambled eggs?
    u: yes
    Alexa: For this recipe you will need a non stick frying pan, a ...are you ready to begin?
    u: no
    Alexa: For this recipe you will need a non stick frying pan, a ...are you ready to begin?

Also consider the following ``states.yml`` definition:

..  code-block:: yaml
    :linenos:

    initialState:
      response:
        shouldEndSession: false
        outputSpeech:
          type: SSML
          ssml: >
            <speak>
              Welcome to simple recipe helper. Would you like to make some scrambled
              eggs?
            </speak>
        reprompt:
          type: SSML
          ssml: >
            <speak>
              Would you like to make some scrambled eggs?
            </speak>
      branches:
        AMAZON.YesIntent: ingredientsScrambledEggs
        default: goodBye

    ingredientsScrambledEggs:
      response:
        shouldEndSession: false
        outputSpeech:
          type: SSML
          ssml: >
            <speak>
              For this recipe you will need a non stick frying pan, a spatula, a
              bowl, a fork, and 2 eggs. Have you located all of these and are you
              ready to begin?
            </speak>
        reprompt:
          type: SSML
          ssml: >
            <speak>
              For this recipe you will need a non stick frying pan, a spatula, a
              bowl, a fork, and 2 eggs. Have you located all of these and are you
              ready to begin?
            </speak>
      branches:
        AMAZON.YesIntent: stepOneScrambledEggs
        AMAZON.NoIntent: ingredientsScrambledEggs
        default: goodBye

..  note::

    Every ``states.yml`` file *must* contain an ``initialState`` block which is the entry point to
    your application

A ``states.yml`` file will contain multiple blocks where each block has a unique name and
corresponds to an Alexa request.

Incoming Request
=================

The request/response cycle will always begin with input from the user. Once the
input is received and assigned an intent, a JSON payload will be sent from the
Alexa platform to your AWS Lambda function.


Examine the Current State
=========================

For the initiating interation, Lazysusan will rely on the ``initialState``
definition to guide the flow of the skill and update the current state when a
response is determined.


Examine the Intent of the Request
=================================

For the initial interaction, there will not be a specific intent provided by the
user, so the state specified for the default branch will be designated as the
current state.


Returning the Response
======================

Once the current state is updated, the response object for that state is
returned to the user.


Example
=======

In the example above we show two blocks. The ``initialState`` block is the response which is
returned upon initial launch of the skill.  The ``ingredientsScrambledEggs`` block will be returned
when the user is in the ``initialState`` state and triggers a ``AMAZON.YesIntent``.

Following this logic, we can see that if the user is in the ``ingredientsScrambledEggs`` state and
triggers an ``AMAZON.NoIntent`` they will be routed back to the same response as
seen in the interaction example above.

Additionally, any undefined intents in a given state will be routed to the ``default`` response.

..  note::

    Every response file *must* contain an ``default`` route/branch

For example, assume we are in ``ingredientsScrambledEggs`` state and the user responds with
something invalid:

::

    Alexa: For this recipe you will need a non stick frying pan, a ...are you ready to begin?
    u: bananas
    Alexa: Goodbye
