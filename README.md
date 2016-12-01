# Lazy Susan

A framework for quickly building Amazon Alexa applications

## Development Recommendations

We highly recommend that you start with one of the example applications. This
will have the environment already setup and configured with everything that you
will need to be able to develop an Alexa skill. Each of these forms also
contains their own read me outlining how to deploy the application and then
modify it. The sky is the limit.

## Development Dependencies

You will need to install Docker, if you are on a mac we recommend using the
Docker for Mac application, and the cmake command line utility. From there, each
example application will have everything else covered.

## Samples

Sample applications are included in the examples folder and contain their own
read me files with directions.

The dad joke example is for an application that does not have session storage
and always executes a random path.

The dad joke 2 example is an example of an application that has local session
storage and will not repeat the same joke back to back times. This will
demonstrate how you can use state in your application to build a full fledged
application.

_Coming Soon_ We are currently working on an example application that uses
DynamoDB for session storage. This is necessary if you need for your session to
live beyond the normal Alexa session lifetime. For example, if you are playing
long form audio, you will need to make use of DynamoDB session storage.
