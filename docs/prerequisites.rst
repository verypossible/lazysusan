.. _prerequisites:

=================================
Prerequisites
=================================

Before using Lazysusan there are a few services along with some software and
hardware tools that you will in order to build skills for Alexa.


Amazon Web Services
===================

Lazysusan has been built so that it can be easily deployed as an `AWS`_ Lambda
function. In order for the deployments to work, you will need an `AWS`_ account
that has admin priviliges along with its public and private keys.

`AWS`_


Amazon Developer Account
========================

In order to deploy an Alexa skill, whether for testing or production use, you
will need to configure a skill store listing for the skill. This listing will
contain information such as how to invoke the skill, how to reach the `AWS`_ Lambda
function you have deployed, your interaction model, along with a console for
testing that allows you to view parsed JSON requests and the responses your
`AWS`_ Lambda function returns.

The `Amazon Developer`_ Account needs to be created with the email address your
Alexa enabled device has been setup with. This is how Alexa knows you are able
to use a skill that has not yet been published.

`Amazon Developer`_


Alexa Enabled Device
====================

The best way to test your application is on the actual hardware people will be
using it with. Therefore you will need to purchase an `Amazon Echo`_ or `Amazon Echo
Dot`_. An alternative is to use the `Reverb.AI`_ service with your phone, tablet, or
computer. With that being said, we recommend using the actual hardware.

`Amazon Echo`_

`Amazon Echo Dot`_

`Reverb.AI`_

Docker
======

So that development with Lazysusan is as effortless as possible, we have created
a container on `Docker`_ hub that will help ease the pain of dependency management.
The container will setup a NodeJS environment that will handle deployments with
serverless along with a Python 2.7 environment so you may execute the Python
REPL and execute any automated test suites that you may write.

`Docker`_


CMake
=====

To keep you from having to script repetitive tasks with shell scripts, we
recommend using `CMake`_ for building your `Docker`_ container, executing deploys, and
running test suites.

`CMake`_

.. _AWS: https://aws.amazon.com/
.. _Amazon Developer: https://developer.amazon.com/
.. _Docker: https://www.docker.com/products/docker
.. _CMake: https://cmake.org/download/
.. _Reverb.AI: https://reverb.ai/
.. _Amazon Echo: https://www.amazon.com/Amazon-Echo-Bluetooth-Speaker-with-WiFi-Alexa/dp/B00X4WHP5E/
.. _Amazon Echo Dot: https://www.amazon.com/All-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room/dp/B01DFKC2SO/
