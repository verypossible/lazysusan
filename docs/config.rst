.. _config:

=====================================
Configuration in the Developer Portal
=====================================

The configuration screen in the Amazon Developer portal tells the Alexa platform
where to send the JSON payload when your skill in invoked by a user. Since the
Lazysusan framework is deployed to AWS Lambda, configuring this section is
relatively trivial.


Endpoint
========

For the endpoint section, make sure the radio button for "AWS Lambda ARN" is
selected, the appropriate region checkbox is checked, and the Amazon Resource
Number (ARN) for your Lambda function is pasted into the corressponding region
text field. If you deploy your Lambda function to multiple regions, you will be
able to check both region checkboxes and supply both ARN numbers.


Account Linking
===============

For the example application, leave the Account Linking radio button set to "No".
If you wish to create a skill that utilizes Account Linking, you will need to
provide the required OAuth criteria.
