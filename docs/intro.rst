.. _intro:

=================================
Introduction
=================================

Lazysusan is a Python framework for authoring Amazon Alexa applications.

At a very high level, Alexa apps are quite simple from a code perspective. The Alexa platform
sends `json` requests to a publicly accessible endpoint (either an https server or AWS Lambda
function) and that endpoint responds with a specific `json` response.

   Lazysusan helps you digest these requests and respond appropriately.


Alexa overview
=================

Covering the details of building apps for Alexa is out of scope for this document. However, we will
cover the very high level details.

Before anything else you must first design an :term:`Interaction model`. This model will map
natural language phrases to an :term:`Intent`. It's important to understand that an :term:`Intent`
is determined by the Alexa platform after listening to the user's speech and working it's magic.
After the Alexa platform has determined what the user's intent is based on what they said, it will
send your endpoint an ``IntentRequest`` with the named ``Intent`` inside of the payload.

Let's look at an example:

::

    {
      "session": {
        "new": false,
        "sessionId": "amzn1.echo-api.session.2a0bb3c1-94a4-4e7e-a631-cb692b573deb",
        "application": {
          "applicationId": "amzn1.ask.skill.234q1bff-d9bd-445b-84ad-f3312ba343aa"
        },
        "user": {
          "userId": "amzn1.ask.account.WWOJTSRCEIMTTKWHGM3YX5HMXQ"
        },
        "attributes": {
          "AGE_STATE": "initialState"
        }
      },
      "request": {
        "locale": "en-US",
        "timestamp": "2016-12-14T00:19:59Z",
        "type": "IntentRequest",
        "requestId": "amzn1.echo-api.request.3de78bf9-f0ab-4353-9528-9ebb6da92ea6",
        "intent": {
          "slots": {
            "dob": {
              "name": "dob",
              "value": "1973-08-15"
            }
          },
          "name": "MyAgeIntent"
        }
      },
      "version": "1.0",
      "context": {
        "AudioPlayer": {
          "playerActivity": "IDLE"
        },
        "System": {
          "device": {
            "supportedInterfaces": {
              "AudioPlayer": {}
            }
          },
          "application": {
            "applicationId": "amzn1.ask.skill.234q1bff-d9bd-445b-84ad-f3312ba343aa"
          },
          "user": {
            "userId": "amzn1.ask.account.WWOJTSRCEIMTTKWHGM3YX5HMXQ"
          }
        }
      }
    }


In this request, the user has triggered a ``MyAgeIntent`` intent with a slot value of
``1973-08-15``.  Each request may or may not have a ``slot``...these are defined in your
:term:`Interaction model` in the Alexa developer portal.

There are several built-in intents which are at your disposal from Amazon. A couple of very basic
examples:

- ``AMAZON.YesIntent``
- ``AMAZON.NoIntent``

As you can likely guess, if a user says ``yes``, ``sure``, ``yes, please`` or any other type of
affirmation, a ``AMAZON.YesIntent`` intent is sent to your endpoint. As the developer, you design
the logic of your Alexa application by looking at the intent of each request and responding
accordingly.


Lazysusan design
====================

Lazysusan is designed mainly around a yaml configuration file which defines how your application
will respond to different intents. Additionally, Lazysusan can keep track of the user's current
state in your application where "state" really means the last used intent.

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
        outputSpeech:
          type: PlainText
          text: What is the best Alexa Python framework?
        shouldEndSession: False
      branches:
        SomeIntent: answerToQuestion
        default: initialState

    answerToQuestion:
      response:
        outputSpeech:
          type: PlainText
          text: Would you like to quit now?
        shouldEndSession: False
      branches:
        AMAZON.YesIntent: goodBye
        default: answerToQuestion

    goodBye:
      response:
        outputSpeech:
          type: PlainText
          text: Thanks for using MyApp, goodbye
        shouldEndSession: True
      branches:
        default: initialState


The exact details for an interaction:

- User launches the Alexa skill (i.e., "Alexa, open MyApp" -> ``LaunchRequest``)
- Lazysusan picks up the ``LaunchRequest`` and maps that to the ``initialState`` response.
  Lazysusan saves the current state as ``initialState``.
- MyApp creates a response based on the contents of the yaml file (i.e.,
  "What is the best Alexa Python framework?")
- User responds to the question and triggers a new Intent (i.e., "Lazysusan" -> ``SomeIntent``)
- MyApp picks up the ``SomeIntent`` in the request. It also knows the current state is
  ``initialState``. Lazysusan finds that it should respond with the ``answerToQuestion`` block with
  this combination of Intent and state. Lazysusan saves the current state as ``answerToQuestion`` and
  responds based on the contents of the ``answerToQuestion`` block in the yaml file.
  (i.e., "Would you like to quit now?")
- User responds to the question and triggers a new Intent (i.e., "yes" -> ``AMAZON.YesIntent``)
- MyApp picks up the ``AMAZON.YesIntent`` in the request. It also knows the current state is
  ``answerToQuestion``. With these two pieces of information it finds that it should reply with the
  ``goodBye`` message.
  (i.e., "Thanks for using MyApp, goodbye")
- Lazysusan saves the current state as ``goodBye`` before sending response

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
      +-----+------+
      | SomeIntent |          # map SomeIntent to answerToQuestion response
      +-----+------+
            |
            |
            v
         response           # current state = answerToQuestion
            |
            |
            v
    +-------+-------+
    | AMZ.YesIntent |       # map AMAZON.YesIntent to goodBye
    +-------+-------+
            |
            v
         response           # current state == goodBye
