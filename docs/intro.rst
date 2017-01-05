.. _intro:

=================================
Introduction
=================================

Lazysusan is a Python framework for authoring Amazon Alexa applications.

At a very high level, Alexa apps are quite simple from a code perspective. The Alexa platform
sends ``json`` requests to a publicly accessible endpoint (either an https server or AWS Lambda
function) and that endpoint responds with a specific ``json`` response.

   Lazysusan helps you digest these requests and respond appropriately.

Lazysusan is designed mainly around a yaml configuration file which defines how your application
will respond to different intents. Additionally, Lazysusan can keep track of the user's current
state in your application where "state" really means the last used intent.

There are two main components in any Lazysusan applicaiton:

- A ``states.yml`` file which defines how users will be directed through your Alexa skill
- A ``handler.py`` file which used the ``LazySusanApp`` class to digest requests and produce
  responses in combination with ``states.yml``

To understand Lazysusan applications and how to author your configuration yaml file it's necessary
to understand how Lazysusan determines the response to send. The following sequence is the process
that Lazysusan uses to determine the approprate response payload:

- Look at the current state
- Grab the matching yaml block for the current state
- Look at the Intent sent in the request
- Find the matching Intent in the ``branches`` map
- Reply with the response for that matching branch or ``default`` if the Intent isn't defined in
  the ``branches`` map

Let's work through a concrete example.

The ``states.yaml`` file which would drive this interaction would look like the following

.. code-block:: yaml

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

The exact details for an interaction:

- User launches the Alexa skill (i.e., "Alexa, open recipe helper" -> ``LaunchRequest``)
- Lazysusan picks up the ``LaunchRequest`` and maps that to the ``initialState`` response.
  Lazysusan saves the current state as ``initialState``.
- RecipeHelper creates a response based on the contents of the yaml file (i.e.,
  "Welcom to simple recipe helper. Would you like to make some scrambled eggs?")
- User responds to the question and triggers a new Intent (i.e., "yes" -> ``AMAZON.YesIntent``)
- MyApp picks up the ``AMAZON.YesIntent`` in the request. It also knows the current state is
  ``initialState``. Lazysusan finds that it should respond with the ``ingredientsScrambledEggs`` block with
  this combination of Intent and state. Lazysusan saves the current state as
  ``ingredientsScrambledEggs`` and
  responds based on the contents of the ``ingredientsScrambledEggs`` block in the yaml file.
  (i.e., "For this recipe you will need a non stick frying pan...are you ready to begin?")
- User responds to the question and triggers another request with a new Intent
  (i.e., "yes" -> ``AMAZON.YesIntent``)
- MyApp picks up the ``AMAZON.YesIntent`` in the request. It also knows the current state is
  ``ingredientsScrambledEggs``. With these two pieces of information it finds that it should reply with the
  ``stepOneScrambledEggs`` message (not shown).
- Lazysusan saves the current state as ``stepOneScrambledEggs`` before sending response

::

      LaunchRequest         # current state == null
            +
            |
            v
     +------+-------+
     | initialState |        # map LaunchRequest to initialState response
     +------+-------+
            |
            |
            v
         response           # current state == initialState
            |
            |
            v
    +-------+-------+
    | AMZ.YesIntent |       # map AMAZON.YesIntent to ingredientsScrambledEggs response
    +-------+-------+
            |
            |
            v
         response           # current state = ingredientsScrambledEggs
            |
            |
            v
    +-------+-------+
    | AMZ.YesIntent |       # map AMAZON.YesIntent to stepOneScrambledEggs
    +-------+-------+
            |
            v
         response           # current state == stepOneScrambledEggs
            |
            |
            v
         CONTINUE


