.. _testing:

=====================================
Testing and Debugging
=====================================

Once you have built out your skill, you have a couple of different options for
testing and debugging.


Developer Portal
================

As you may have noticed, there is a testing screen within the developer portal.
On this screen you are able to enable and disable your skill for testing on
Alexa enabled devices (we recommend that you always leave this option enabled
and create different production and development versions of your skill). There
is also a voice simulator so that you can hear how Alexa will pronounce certain
output before you update and deploy.

The most helpful feature on this screen is the service simulator. Here are you
able to enter your sample utterances, or variations of them, to see what the
JSON request and the JSON response from your AWS Lambda function will look like.
You can test this out with the example skill by typing in "how about scrambled
eggs". You should then see the Lambda request and Lambda response fields
populate once you press the "Ask Recipe Helper" button.


Alexa Enabled Device
====================

Once your skill is deployed, you can invoke the skill on your Alexa enabled
devices as long as the Amazon Developer portal and Alexa app accounts that you
are using are the same Amazon account. To invoke your skill say "Alexa, tell
recipe helper that I need help making scrambled eggs." Once the Alexa device
performs the network request and receives a response, you should hear the output
that you specified in your states.yml file.


Cloud Watch
===========

If you have the ``LAZYSUSAN_LOG_LEVEL`` environment variable for your AWS Lambda
function set to ``logging.INFO`` you will be able to read fairly detailed logs
that have been created by your Alexa skill.
