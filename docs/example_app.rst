.. _example_app:

===============================
Example Application
===============================

Using Lazysusan may be best explained by walking through an example. In this example, we'll build
an Alexa skill which walks you through the steps on how to fry an egg.


Docker setup
=====================

As noted in the :ref:`intro`, using Docker isn't required but it can make your life easier and get
you up and running faster. Our Docker image is set up with:

- `Serverless`_
- Python 2.7 and some helper packages

Assuming you have Docker installed on your system, pull the `joinspartan/serverless`_ image. It's
suggested you use a specific  tag which corresponds to a specific version of Serverless. Here,
we'll be using ``1.4``:

::

    $ docker pull joinspartan/serverless:1.4


Repo setup
=============

Let's add some of the boilerplate and get ready to write our applicaiton:

::

    $ mkdir fried_eggs
    $ cd fried_eggs

There are a few things we'll need to do multiple times such as deploying our application to AWS
Lambda, updating supporting libraries, etc. The ``Makefile`` will make most common tasks much
easier and also set you up to deploy your Lambda functions to different "environments" with
different variables.

This ``Makefile`` will be the first file in the ``fried_eggs`` directory:

::

    NAME = "joinspartan/serverless:1.4"

    ENVDIR=envs
    LIBS_DIR=src/lib


    .PHONY:	libs shell env-dirs tests deploy function check-env

    run = docker run --rm -it \
            -v `pwd`:/code \
            --env ENV=$(ENV) \
            --env-file envs/$2 \
            --name=age-serverless-$(ENV) $(NAME) $1


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
    docker run --rm -it -v `pwd`:/code --env ENV=dev --env-file envs/dev --name=age-serverless-dev "joinspartan/serverless:1.4" bash
    root@9fcf3335e5aa:/code#
    root@9fcf3335e5aa:/code# sls create --template aws-python -p src -n fried_eggs

You can see both in the container and on your local host system that ``src`` directory was created
with two files:

::

    $ ls -l src/
    -rw-r--r--   1 brianz  staff   490 Jan  4 11:54 handler.py
    -rw-r--r--   1 brianz  staff  2308 Jan  4 11:54 serverless.yml

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

Line 12 sets an environment variable for session storage.  By default sessions will use DynamoDB as
a storage backend...this requires additional setup which we don't need in this example application.
By using ``cookie`` the sessions are stored in the request/response cycle of the Alexa application.
This allows us a very short-term session storage...as long as the application is executing and the
user is interacting with the application the session is alive.  As soon as an application quits the
session is erased.

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
    service: FriedEggs
    stage: dev
    region: us-east-1
    api keys:
      None
    endpoints:
      None
    functions:
      FriedEggs-dev-recipes: arn:aws:lambda:us-east-1:234123421348:function:FriedEggs-dev-recipes

Make note of the Lambda ``arn`` in the last line. This is the ``arn`` which you'll need to plug
into your Alexa skill's "Configuraton -> Endpoint"


Iteration
============

Once the initial deploy is done you'll likely be updating code and need to redeploy. This can be
accomplished by using the ``make function`` target.  This will re-upload your application code to
the Lambda function and takes 5-10 seconds usually.

If you make any changes to the actual stack, (i.e., adding a DynamoDB table or the like) you'll
want to do an ``make deploy`` again.


Configuring Alexa
==================

At this point your backend system is fully ready to handle Alexa requests. Provided your Alexa app
is configured correctly everything should be working.


.. _Serverless: https://serverless.com
.. _joinspartan/serverless: https://hub.docker.com/r/joinspartan/serverless/
