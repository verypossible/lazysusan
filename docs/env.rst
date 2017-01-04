.. _env:

===============================
Environment Variables
===============================

So that you don't have to write a lot of code to change the applications
behavior, there are several environment variables that are a part of the
Lazysusan framework that allow you to alter functionality without having to
write additional code.


AWS_ACCESS_KEY_ID
=================

This environment variable is required by serverless so skill logic can be
deployed to AWS Lambda. This information can be obtained from AWS when
generating access keys for a specific user.


AWS_SECRET_ACCESS_KEY_ID
========================

This environment variable is required by serverless so skill logic can be
deployed to AWS Lambda. This information can be obtained from AWS when
generating access keys for a specific user.


AWS_REGION
=================

This environment variable is required by serverless to ensure the skill logic is
deployed to the correct region in AWS. For now, this should be set to
``us-east-1``.


DEV_NAME
========

This environment variable is optional, but helpful so that when you are running
a docker container you can verify which environment will be updated during a
deployment.


LAZYSUSAN_LOG_LEVEL
===================

This environment variable is optional and determines the log level of the AWS
Lambda function. The available values for this environment variable are the
standard Python logging levels. If a log level is not specified,
``logging.WARN`` will be used as the default.


LAZYSUSAN_SESSION_STORAGE_BACKEND
=================================

This evironment variable is optional and determines how Lazysusan sessions will
be handled throughout the skill lifecycle. They available values are:

``memory``: No session information will be tracked, the ``initialState`` will be
used to drive all state transition throughout the skill.

``cookie``: With this setting, session information will live in the request -
response lifecycle so that state transitions can occur. All session information
is lost when skill execution is terminated.

``dynamodb``: This is the default setting if a value is not specified. With this
setting, session information will be stored in DynamoDB so session information
can live beyond the execution of the skill. This is particularly useful when
playing long audio as the skill execution is terminated when the long audio is
playing and audio playback metadata needs to be stored so that it can be resumed
if needed.


LAZYSUSAN_SESSION_DYNAMODB_TABLE_NAME
=====================================

This environment variable is required when ``LAZYSUSAN_SESSION_STORAGE_BACKEND``
is set to ``dynamodb``. This allows serverless to create the appropriate
DynamoDB table as well as allows the skill logic to properly access the DynamoDB
table.


LAZYSUSAN_SESSION_AWS_REGION
============================

This environment variable is required when ``LAZYSUSAN_SESSION_STORAGE_BACKEND``
is set to ``dynamodb``. This is used for finding the DynamoDB table that is set
in ``LAZYSUSAN_SESSION_DYNAMODB_TABLE_NAME``.


LAZYSUSAN_TTL_SECONDS
=====================

This environment variable is optional. It is used when
``LAZYSUSAN_SESSION_STORAGE_BACKEND`` is set to ``dynamodb`` and must be set to
a positive integer. This allows the developer to specify a length of time that
session information stored in DynamoDB is valid. The default value for this
environment variable is ``0`` which means that a session is indefinitely valid.
