FROM node

ENV SERVERLESS_VERSION 1.3.0

RUN npm install serverless@${SERVERLESS_VERSION} -g

RUN apt-get update
RUN apt-get install -y \
    build-essential \
    curl \
    python-dev

RUN mkdir /root/.aws

RUN curl -s https://bootstrap.pypa.io/get-pip.py | python
RUN pip install \
    awscli \
    pep8 \
    pytest \
    pytest-cov \
    pytest-mock \
    boto3

RUN pip install git+https://github.com/spartansystems/lazysusan.git

RUN echo "alias ll='ls -alFh'" >> /root/.bashrc

RUN mkdir /code
WORKDIR /code
