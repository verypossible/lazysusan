.. _example_app:

===============================
Example Application
===============================

Now that we have covered the basics, here is a step by step example that goes
through how to create a simple Lazysusan application. Since all of the topics have
already been covered, this will mostly be a lot of terminal commands and files
to copy and paste.


Repo setup
=============

Let's add some of the boilerplate and get ready to write our application:

::

    $ mkdir recipe_helper
    $ cd recipe_helper


Docker setup
=====================

As noted in the :ref:`intro`, using Docker isn't required but it can make your life easier and get
you up and running faster. Our Docker image is set up with:

- `Serverless`_
- Python 2.7 and some helper packages

Assuming you have Docker installed on your system, pull the `joinspartan/serverless`_ image. It's
Suggested you use a specific  tag which corresponds to a specific version of Serverless. Here,
we'll be using ``1.4``:

::

    $ docker pull joinspartan/serverless:1.4


Makefile
===============

There are a few things we'll need to do multiple times such as deploying our application to AWS
Lambda, updating supporting libraries, etc. The ``Makefile`` will make most common tasks much
easier and also set you up to deploy your Lambda functions to different "environments" with
different variables.

This ``Makefile`` will be the first file in the ``recipe_helper`` directory:

::

    NAME = "joinspartan/serverless:1.4"

    ENVDIR=envs
    LIBS_DIR=src/lib


    .PHONY:	libs shell env-dirs tests deploy function check-env

    run = docker run --rm -it \
            -v `pwd`:/code \
            --env ENV=$(ENV) \
            --env-file envs/$2 \
            --name=recipe-helper-serverless-$(ENV) $(NAME) $1


    libs :
        @test -d $(LIBS_DIR) || mkdir -p $(LIBS_DIR)
        rm -rf $(LIBS_DIR)/*
        pip install -t $(LIBS_DIR) PyYAML
        @test -f $(LIBS_DIR)/_yaml.so && rm $(LIBS_DIR)/_yaml.so
        pip install -t $(LIBS_DIR) python-dateutil
        pip install -t $(LIBS_DIR) --no-deps -U git+https://github.com/spartansystems/lazysusan.git

    shell : check-env env-dirs
        $(call run,bash,$(ENV))

    env-dirs :
        @test -d $(ENVDIR)

    tests : check-env
        $(call run,py.test tests,$(ENV))

    # NOTE:
    #
    # 	Deployments assume you are already running inside the docker container
    #
    #
    deploy : check-env
        cd src && sls deploy -s $(ENV)

    function : check-env
        cd src && sls deploy -s $(ENV) function -f age

    # Note the ifndef must be unindented
    check-env:
    ifndef ENV
        $(error ENV is undefined)
    endif


Env setup
===========

The next step is getting the minimum set of environment variables set up.  The ``Makefile`` above
is set up to work with different "environments"...examples of this may be "dev", "qa" and
"production". Using "environments" is a method of developing in different systems/stacks so that
you can manage and release code without harming or overwriting a stable stack such as "production".

Let's start by simply creating a single "environment" called ``dev``:

::

    $ mkdir envs
    $ touch envs/dev

At a very minimum you'll need the following AWS environment variables in the environment file.
Here, I'll put the following into the ``envs/dev`` file. Of course, you'll need to put your own AWS
credentials in this file:

::

    AWS_REGION=us-east-1
    AWS_SECRET_ACCESS_KEY=abc123saUMOVIENOWPLEASE3asasdf
    AWS_ACCESS_KEY_ID=1BE3PQTZO872U6

.. note::

   As of this writing AWS Lambda functions used with Alexa **must** be deployed to the
   ``us-east-1`` Northern Virginia region


Bootstrap application
======================

Now, we can start a Docker container and start bootstrapping our application:

::

    $ ENV=dev make shell
    docker run --rm -it -v `pwd`:/code --env ENV=dev --env-file envs/dev --name=recipe-helper-serverless-dev "joinspartan/serverless:1.4" bash
    root@9fcf3335e5aa:/code#
    root@9fcf3335e5aa:/code# sls create --template aws-python -p src -n recipe_helper

You can see both in the container and on your local host system that ``src`` directory was created
with two files:

::

    $ ls -l src/
    -rw-r--r--   1 user  staff   490 Jan  4 11:54 handler.py
    -rw-r--r--   1 user  staff  2308 Jan  4 11:54 serverless.yml

We'll edit these files soon.  Next, we'll need to setup our supporting libraries which are dependencies for your application
code.  These are listed out in the ``Makefile`` :makevar:`libs` directive.

In the container or on your local system run ``make libs``

::

    root@9fcf3335e5aa:/code# make libs
    rm -rf src/lib/*
    pip install -t src/lib PyYAML
    ....
    Successfully installed lazysusan-0.6

There is now a ``src/lib`` folder which contains the supporting libraries code.


Application code
=======================

Open up ``handler.py`` and replace it with the following.  We'll walk through what each line does
but in short this is all of the code you'll need for a basic Lazysusan app.

.. code-block:: python
   :linenos:

   import os
   import sys

   CWD = os.path.dirname(os.path.realpath(__file__))
   sys.path.insert(0, os.path.join(CWD, "lib"))

   from lazysusan import LazySusanApp


   def main(event, lambda_context):
       state_path = os.path.join(CWD, "states.yml")
       os.environ["LAZYSUSAN_SESSION_STORAGE_BACKEND"] = "cookie"
       app = LazySusanApp(state_path, session_key="FRIED_EGGS_STATE")
       response = app.handle(event)
       return response

Because we're deploying our application code to AWS Lambda there is some system path munging needed
in order for our application to find the needed libraries.  Lines 4-5 simple add the ``lib/``
directory to Lambda system path. You may recall that the ``lib/`` directory is where we installed
our supporting packages such as ``lazysusan``.

.. note::

   Any third party libraries which you install in ``lib/`` **must** be imported **after** the path
   munging. This is why the ``lazysusan`` import occurs after the call to ``sys.path.insert``


AWS Lambda will call a single function when invoked.  We'll configure this in the
``serverless.yml`` file in the next section.  It should be obvious that there is only one function
which is our entry point into the application.

One line 11 we tell Lazysusan where our main ``states.yml`` file is.  This file is criticial and
defines the flow of our Alexa application in terms of the Voice User Interface.

Line 12 sets an environment variable for session storage. By default sessions will use DynamoDB as
a storage backend...this requires additional setup which we don't need in this example application.
By using ``cookie`` the sessions are stored in the request/response cycle of the Alexa application.
This allows us a very short-term session storage...as long as the application is executing and the
user is interacting with the application the session is alive. As soon as an application quits the
session is erased.

.. note::

  Line 12 could be removed and set using the environment variable file. However,
  this would require some changes to the serverless deployment process so the
  environment variable is properly set in the AWS Lambda function.

Lines 13-15 are quite simple.  The only thing to note is that you should set the ``session_key``
variable to something which makes sense for your application.  This is the name of the key which
stores the current state for a user in the session backend. This isn't important when using the
``cookie`` backend, however when using the ``dynamodb`` backend you will actually see this named
key in DynamoDB...so it's nice to have it named something which is clear and makes sense.


serverless.yml
====================

Next we need to configure Serverless to set up our Lambda function correctly.  Crack open the
generated ``serverless.yml`` file and replace the contents with the following:

.. code-block:: yaml
   :linenos:

   service: Recipes

   provider:
     name: aws
     runtime: python2.7
     region: ${env:AWS_REGION}
     memorySize: 128

   package:
     exclude:
       - "**/*.pyc"
       - "**/*.swp"

   functions:
     recipes:
       handler: handler.main
       events:
         - alexaSkill


States
=========

In the ``src`` directory, create a file called ``states.yml`` with the following
content:

.. code-block:: yaml
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

  stepOneScrambledEggs:
    response:
      shouldEndSession: false
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            Without getting the egg shell into the bowl, crack the first egg into
            the bowl.
            <break time="3s" />
            Repeat this for the second egg.
            <break time="3s" />
            Are you ready for the next step?
          </speak>
      reprompt:
        type: SSML
        ssml: >
          <speak>
            Without getting the egg shell into the bowl, crack the first egg into
            the bowl.
            <break time="3s" />
            Repeat this for the second egg.
            <break time="3s" />
            Are you ready for the next step?
          </speak>
    branches:
      AMAZON.YesIntent: stepTwoScrambledEggs
      AMAZON.NoIntent: stepOneScrambledEggs
      default: goodBye

  stepTwoScrambledEggs:
    response:
      shouldEndSession: false
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            Take the fork and whisk the eggs in the bowl until the egg yolks are
            mixed with the egg whites.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
      reprompt:
        type: SSML
        ssml: >
          <speak>
            Take the fork and whisk the eggs in the bowl until the egg yolks are
            mixed with the egg whites.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
    branches:
      AMAZON.YesIntent: stepThreeScrambledEggs
      AMAZON.NoIntent: stepTwoScrambledEggs
      default: goodBye

  stepThreeScrambledEggs:
    response:
      shouldEndSession: false
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            Pour the beaten eggs into the non stick frying pan.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
      reprompt:
        type: SSML
        ssml: >
          <speak>
            Pour the beaten eggs into the non stick frying pan.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
    branches:
      AMAZON.YesIntent: stepFourScrambledEggs
      AMAZON.NoIntent: stepThreeScrambledEggs
      default: goodBye

  stepFourScrambledEggs:
    response:
      shouldEndSession: false
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            Take the non stick frying pan and place it on one of the eyes of your
            cook top. Make sure to turn on the eye to low heat.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
      reprompt:
        type: SSML
        ssml: >
          <speak>
            Take the non stick frying pan and place it on one of the eyes of your
            cook top. Make sure to turn on the eye to low heat.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
    branches:
      AMAZON.YesIntent: stepFiveScrambledEggs
      AMAZON.NoIntent: stepFourScrambledEggs
      default: goodBye

  stepFiveScrambledEggs:
    response:
      shouldEndSession: false
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            Occasionally stir and flip the eggs in the frying pan with your
            spatula to make sure they cook evenly while slightly increasing the
            heat of the cooking eye once every minute.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
      reprompt:
        type: SSML
        ssml: >
          <speak>
            Occasionally stir and flip the eggs in the frying pan with your
            spatula to make sure they cook evenly while slightly increasing the
            heat of the cooking eye once every minute.
            <break time="5s" />
            Are you ready for the next step?
          </speak>
    branches:
      AMAZON.YesIntent: stepSixScrambledEggs
      AMAZON.NoIntent: stepFiveScrambledEggs
      default: goodBye

  stepSixScrambledEggs:
    response:
      shouldEndSession: true
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            The scrambled eggs will be done when they are no longer runny. When
            they are done, transfer them to a plate and enjoy.
            <break time="5s" />
            Thanks for trying simple recipe helper.
          </speak>

  goodBye:
    response:
      shouldEndSession: true
      outputSpeech:
        type: SSML
        ssml: >
          <speak>
            Thanks for trying simple recipe helper.
          </speak>


Deploy
===========

With that, everything is ready to create our stack and Lambda function. Inside the Docker container
in the same directory as the ``Makefile`` we'll execute ``make deploy``:

::

    root@9fcf3335e5aa:/code# make deploy
    cd src && sls deploy -s dev
    Serverless: Creating Stack...
    Serverless: Checking Stack create progress...
    .....
    Serverless: Stack create finished...
    Serverless: Packaging service...
    Serverless: Uploading CloudFormation file to S3...
    Serverless: Uploading service .zip file to S3 (272.67 KB)...
    Serverless: Updating Stack...
    Serverless: Checking Stack update progress...
    ...................
    Serverless: Stack update finished...
    Service Information
    service: Recipes
    stage: dev
    region: us-east-1
    api keys:
      None
    endpoints:
      None
    functions:
      Recipes-dev-recipes: arn:aws:lambda:us-east-1:234123421348:function:Recipes-dev-recipes

Make note of the Lambda ``arn`` in the last line. This is the ``arn`` which you'll need to plug
into your Alexa skill's "Configuraton -> Endpoint"


Iteration
============

Once the initial deploy is done you'll likely be updating code and need to redeploy. This can be
accomplished by using the ``make function`` target.  This will re-upload your application code to
the Lambda function and takes 5-10 seconds usually.

If you make any changes to the actual stack, (i.e., adding a DynamoDB table, updating an envrionment
variable, or the like) you'll want to do an ``make deploy`` again.


Configuring Alexa
==================

At this point your backend system is fully ready to handle Alexa requests. Provided your Alexa app
is configured correctly in the Amazon Developer portal everything should be working.


Cloud Watch
===========

If you have the ``LAZYSUSAN_LOG_LEVEL`` environment variable for your AWS Lambda
function set to ``logging.INFO`` you will be able to read fairly detailed logs
that have been created by your Alexa skill.

.. _Serverless: https://serverless.com
.. _joinspartan/serverless: https://hub.docker.com/r/joinspartan/serverless/
