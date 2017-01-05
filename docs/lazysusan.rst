.. _lazysusan:

============================
Lazysusan programming model
============================

The Lazysusan framework mostly revolves around a yaml file where you configure how your Alexa skill
should behave. As noted in the :ref:`intro-design` section Lazysusan will inspect the user's
current state, current Intent and then lookup how to respond to the request.

There are different classes of responses which Lazysusan supports:

- Static
- Dynamic


Static responses
=================

In a very simple Alexa skill responses will be static, meaning they are predetermined and never
change. An example of this would be our scrambled eggs example:

::

    user: Alexa, ask recipe helper how to make scrambled eggs
    Alexa: Welcome to simple recipe helper. Would you like to make some scrambled eggs?

In this example the steps to make scrambled eggs will never change.

To build an app such as this we simply define the responses in a file names ``states.yml``.  This
file may be named anything really...eventually you will put the name and full path to this file in
your application code so Lazysusan can read it.

Let's take a look at an example file and walk through the details

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

In the example above we show two blocks. The ``initialState`` block is the response which is
returned upon initial launch of the skill.  The ``ingredientsScrambledEggs`` block will be returned
when the user is in the ``initialState`` state and triggers a ``AMAZON.YesIntent``.

Following this logic, we can see that if the user is in the ``ingredientsScrambledEggs`` state and
triggers an ``AMAZON.NoIntent`` they will be routed back to the same response. For example:

::

    user: Alexa, ask recipe helper how to make scrambled eggs
    Alexa: Welcome to simple recipe helper. Would you like to make some scrambled eggs?
    u: yes
    Alexa: For this recipe you will need a non stick frying pan, a ...are you ready to begin?
    u: no
    Alexa: For this recipe you will need a non stick frying pan, a ...are you ready to begin?

Additionally, any undefined intents in a given state will be routed to the ``default`` response.

..  note::

    Every response file *must* contain an ``default`` route/branch

For example, assume we are in ``ingredientsScrambledEggs`` state and the user responds with
something invalid:

::

    Alexa: For this recipe you will need a non stick frying pan, a ...are you ready to begin?
    u: bananas
    Alexa: Goodbye


Response format
===================

Lazysusan doesn't add any syntactic sugar or do any checking of the responses defined in your
``states.yml`` file.  The structure defined in your file is sent back as a response (mostly)
unadulterated.  Therefore, it's your responsibility to make sure the response is valid and structured
properly according to Amazon's latest specs.

States can be declared using this format:

::

  stateName:
    response:
      ...
    is_state: [True|False]
    branches:
      ...

The ``stateName`` is required as it is how each state is identified. These names
are also used when defining ``branches``.

Underneath the ``stateName`` there are three possible key choices: ``response``,
``is_state``, and ``branches``.

response
--------

The ``response`` key is the response that is returned to the Alexa device.
Lazysusan will not perform any major alterations to this construct other than
converting it to JSON to be returned to the requesting device. Therefore, it is
your responsibility to make sure your responses adhere to the Alexa platform
schema for defining a response. This is extremely powerful because you are able
to use the latest API functionality from Amazon without needing to update
Lazysusan.

is_state
--------

This key will default to ``True`` so you only need to set it if you need value
to be ``False``. When ``is_state`` is set to ``False``, the response will be
returned, but the cookie or DynamoDB session will not be updated and state
transition will not occur. This is primarily used when dealing with long form
audio callbacks.

branches
--------

Underneath the branches key will be a list of intent - state pairs. These are
used to say that when I am in state ``stateName`` and the user has invoked
intent ``A``, transition to the state for intent ``A`` or fallback to the
``default``. It is recommended to always provide a ``default`` branch unless
skill execution is terminated at this state.


Dynamic responses
=================

# TODO
