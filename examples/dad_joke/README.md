# Sample Alexa Skill: Bad Dad Jokes

This example is an application that does not store any kind of session
information at all. All branches are controlled from the initial state.

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
            "intent": "MySimpleLaunchIntent"
        },
        {
            "intent": "AMAZON.YesIntent"
        },
          {
            "intent": "AMAZON.NoIntent"
        }
    ]
}
```

Sample utterances
```
MySimpleLaunchIntent open
```

Once you have everything filled out, you should be able to test on an alexa
capable device or within the amazon developer portal.

## Adding another dad joke

Edit the `states.yml` file to add

```yaml
kleenexPath:
  response:
    card:
      type: Simple
      title: Kleenex
      content: >
        How do you get a kleenex to dance?
        Put a little boogie in it.
    outputSpeech:
      type: SSML
      ssml: >
        <speak>
          How do you get a kleenex to dance?
          <break time="1s" />
          Wait for it.
          <break time="1s" />
          Put a little boogie in it.
        </speak>
    shouldEndSession: True

```

Edit the `callbacks/random_joke.py` module to add `kleenexPath` to the list of
available random jokes. Then follow the deploy steps.
