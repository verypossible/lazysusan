.. _prerequisites:

=================================
Prerequisites
=================================

Before using Lazysusan there are a few services along with some software and
hardware tools that you will in order to build skills for Alexa.


Amazon Web Services
===================

Lazysusan has been built so that it can be easily deployed as an `AWS`_ Python Lambda
function. In order for the deployments to work, you will need an `AWS`_ account
that has admin priviliges along with its public and private keys.


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


Alexa Enabled Device
====================

The best way to test your application is on the actual hardware people will be
using it with. Therefore you will need to purchase an `Amazon Echo`_ or `Amazon Echo
Dot`_. An alternative is to use the `Reverb.AI`_ service with your phone, tablet, or
computer. With that being said, we recommend using the actual hardware.


Python 2.7
============

Since Lazysusan is a Python framework you'll need a Python 2.7 environment for testing and
development. If you decide to use our Docker image this is already set up for you.


Docker
======

So that development with Lazysusan is as effortless as possible, we have created
a `Docker`_ image that will help ease the pain of dependency management. See the
`joinspartan/serverless`_ image on Docker Hub.
The container will setup a NodeJS environment that will handle deployments with
the `Serverless`_ framework with a Python 2.7 environment so you may execute the Python
REPL and execute any automated test suites that you may write.

Using Docker isn't absolutely required, but makes development and deployment much much easier
thanks in part to Serverless. If you'd like to run Serverless on a local system that will work as
well.


Make
=====

To keep you from having to script repetitive tasks with shell scripts, we
recommend using gnu ``Make`` for executing deploys,
running test suites and other repetitive tasks. We'll show an example
``Makefile`` on how this is useful. Just like Docker, this is optional.


.. _AWS: https://aws.amazon.com/
.. _Amazon Developer: https://developer.amazon.com/
.. _Docker: https://www.docker.com/products/docker
.. _joinspartan/serverless: https://hub.docker.com/r/joinspartan/serverless/
.. _Serverless: https://serverless.com
.. _Reverb.AI: https://reverb.ai/
.. _Amazon Echo: https://www.amazon.com/Amazon-Echo-Bluetooth-Speaker-with-WiFi-Alexa/dp/B00X4WHP5E/
.. _Amazon Echo Dot: https://www.amazon.com/All-New-Amazon-Echo-Dot-Add-Alexa-To-Any-Room/dp/B01DFKC2SO/
