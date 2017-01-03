.. _intro:

=================================
Introduction
=================================

Lazysusan is a Python framework for authoring Amazon Alexa applications. At a very high level, Alexa
apps are quite simple from a code perspective. The Alexa platform sends `json` requests to a
publicly accessible endpoint (either an https server or AWS Lambda function) and that endpoint
responds with a specific `json` response.

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
``1973-08-15``.
