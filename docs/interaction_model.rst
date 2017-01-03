.. _interaction_model:

=================================
Defining the Interaction Model
=================================

The interaction model tells the Alexa platform how users can interact with the
skills you build. The three parts of the interaction model are the intent
schema, custom slot types, and sample utterances.


The Intent Schema
=================

The intent schema is a JSON listing of intents that a user may have while using
your skill. In other words, the Alexa platform will process the voice input from
the users, perform a text to speech translation, and then identify the type of
action the user wants your skill to take. The Alexa platform is able to
designate an intent for the user's input from training it receives from the
sample utterances. Throughout the course of building this sample application, we
are going to focus on using the default ``AMAZON.YesIntent`` and
``AMAZON.NoIntent``. Don't be afraid, Amazon provides more built in intents in
the Alexa platform as well as gives you the ability to define your own intents.

Here is an example of how the yes and no intents can be included in your skill
along with a custom intent of your own:

::

  {
    "intents": [
      { "intent": "AMAZON.YesIntent" },
      { "intent": "AMAZON.NoIntent" },
      { "intent": "MyCustomIntent" }
    ]
  }


Custom Slot Types
=================

Sample Utterances
=================
