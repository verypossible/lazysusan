.. _lazysusan:

===================================
Lazysusan application structure
===================================

The Lazysusan framework mostly revolves around a yaml file where you configure how your Alexa skill
should behave. As noted in the :ref:`intro` section Lazysusan will inspect the user's
current state, current Intent and then lookup how to respond to the request.

There are different classes of responses which Lazysusan supports:

- `Static responses`_
- `Dynamic responses`_


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

..  note::

    Every ``states.yml`` file *must* contain an ``initialState`` block which is the entry point to
    your application

A ``states.yml`` file will contain multiple blocks where each block has a unique name and
corresponds to an Alexa request.


Defining States
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

There are two types of dynamic responses:

- `Dynamically Returning a State`_
- `Return a Computed Response`_

Both types of callbacks are refenced the same way in your ``states.yml`` file.
In the ``branches`` section of the desired state, for the desired intent, you
will reference your callback using the following format:

::

  !!python/name:callbacks.name_of_function

This format assumes that you have a ``callbacks`` folder for all of your dynamic
responses and that all of them can be retrieved from the ``__init__.py`` file.

Dynamically Returning a State
-----------------------------

The easiest class of dynamic responses is taking slot value input and then
returning the desired static state for that input. For example you could have a
callback function defined as:

..  code-block:: python
    :linenos:

    def choose_recipe(request, *args, **kwargs):
        slot = (request.get_slot_value("Recipes")).lower()

        if "scrambled" in slot:
            return "ingredientsScrambledEggs"
        if ("fried" in slot or "fry" in slot):
            return "ingredientsFriedEggs"

        return "invalidChoosePath"

This assumes that if you will have ``ingredientsScrambledEggs`` and
``ingredientsFriedEggs`` states defined in your ``states.yml`` file and will
tell the framework to transition to that state.


Return a Computed Response
--------------------------

For more complex responses, you can write a callback function that will modify a
predefined shell state, which you will need to define in your ``states.yml``
file, for computed responses. An example callback function may look like:

..  code-block:: python
    :linenos:

    import yaml
    from lazysusan.logger import get_logger
    from lazysusan.response import build_response_payload


    def compute_recipe(offset=0, **kwargs):
        request = kwargs["request"]
        session = kwargs["session"]
        state_machine = kwargs["state_machine"]
        log = get_logger()

        log.debug("Set Computed Recipe")
        response = state_machine["preDefined"]["response"]

        response["outputSpeech"]["SSML"] = """
          <speak>
            This is some dummy content to show that you can return a dynamic
            response.
          </speak>
        """

        session.update_state("goodBye")
        return build_response_payload(response, session.get_state_params())

While this is a fairly simple example, there are a few things to take note of.

First, since this is a Python function, you can perform any calculations, api calls,
etc. that you need to make in or to generate a response.

Second, ``state_machine["preDefined"]`` is defined in your ``states.yml`` file
and you have full access to it. This way you can get some boilerplate definition
out of the way, or you can do it the hard way and define the dict within this
function.

Third, you are responsible for updating the state. This allows you to perform
more fine tuned state transitions.

Finally, you are responsible for building the response payload. We have written
a helper function build this for you.
