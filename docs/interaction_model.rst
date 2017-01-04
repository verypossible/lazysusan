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

When the Alexa platform assigns an intent to a user's input, you only receive
that intent token in the JSON payload for your application. In a way this is a
good thing because you are able to easily provide output for a wide range of
input, but you aren't provided a means to accept more information about the
user's intent. For example, if a user were to say "Alexa, ask recipe helper how
to make scrambled eggs." Then if another user said "Alexa, tell recipe helper
that I need help making fried eggs." How would you tell if a user wanted to make
scrambled eggs or fried eggs? Your knee jerk reaction may be to create a
different intent for each of these sayings, but doing so is risky because the
Alexa platform may assign the wrong intent to the users input. This can be
avoided by using custom slot types.

Custom slot types allow you to define an array of key words that you are
searching for in a user's input. Therefore in the previous example, you can use
the same intent for both phrases, and assign "scrambled eggs" and "fried eggs"
to the ``RECIPE_NAMES`` slot type. This allows you to gain more context on the
user's intent for further processing.

Custom slot types can be created on the interaction model screen by clicking on
the "Add Slot Type" button and then providing a space delimited list of the
keywords that you are looking for. In order to associate a custom slot type with
an intent, you can modify the intent schema like the following example:

::

  {
    "intents": [
      { "intent": "AMAZON.YesIntent" },
      { "intent": "AMAZON.NoIntent" },
      {
        "intent": "MyCustomIntent",
        "slots": [
          {
            "name": "Recipe",
            "type": "RECIPE_NAMES"
          }
        ]
      }
    ]
  }

This tells the Alexa platform that whenever ``MyCustomIntent`` is invoked by the
user to look for a phrase that matches a value in ``RECIPE_NAMES``.


Sample Utterances
=================
