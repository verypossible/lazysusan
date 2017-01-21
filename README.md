# Lazy Susan

[![CircleCI](https://circleci.com/gh/spartansystems/lazysusan.svg?style=svg)](https://circleci.com/gh/spartansystems/lazysusan)
[![Code Climate](https://codeclimate.com/repos/5882a6b6df5c471a36003b3f/badges/6b8c732748aebecf1933/gpa.svg)](https://codeclimate.com/repos/5882a6b6df5c471a36003b3f/feed)
[![Test Coverage](https://codeclimate.com/repos/5882a6b6df5c471a36003b3f/badges/6b8c732748aebecf1933/coverage.svg)](https://codeclimate.com/repos/5882a6b6df5c471a36003b3f/coverage)
[![Issue Count](https://codeclimate.com/repos/5882a6b6df5c471a36003b3f/badges/6b8c732748aebecf1933/issue_count.svg)](https://codeclimate.com/repos/5882a6b6df5c471a36003b3f/feed)

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

The age example is an example application that demonstrates returning
dynamically generated content to be spoken by the alexa enabled device. This
could also be used to read data directly from an external API. This example also
demonstrates how to setup the application to use DynamoDB for session storage
and how to set and retrieve values from DynamoDB.
