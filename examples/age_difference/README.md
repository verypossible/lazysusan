# Sample Alexa Skill: Age Calc

This application demonstrates how a callback can be used to give the user
dynamically generated responses. While this does not hit an API, it certainly
could be used to hit an api and provide the user with custom feedback.

## Deploy

```bash
$ cd examples/dad_joke
$ mkdir -p envs/docker
$ touch envs/docker/dev

edit the dev env file

$ make
$ make libs
$ ENV=dev make shell

inside of docker

$ make deploy
```

Sample dev environment file
```
AWS_ACCESS_KEY_ID=####################
AWS_SECRET_ACCESS_KEY=########################################
AWS_REGION=us-east-1
DEV_NAME=development
```

## Test on a device

Inside of the amazon developer portal, create a new skill.

Intents
```
{
  "intents": [
    {
      "intent": "MyAgeIntent",
        "slots": [{
          "name": "dob",
          "type": "AMAZON.DATE"
        }]
    }
  ]
}
```

Sample utterances
```
MyAgeIntent my birthday is {dob}
MyAgeIntent i was born on {dob}
MyAgeIntent it is {dob}
```

Once you have everything filled out, you should be able to test on an alexa
capable device or within the amazon developer portal.

## Modify the output

Edit the `callbacks/__init__.py` module to modify the response that is given to
the user.
