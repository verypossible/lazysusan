# Sample Alexa Skill: Age Calc

This application demonstrates how a callback can be used to give the user
dynamically generated responses. While this does not hit an API, it certainly
could be used to hit an api and provide the user with custom feedback.

## Deploy

```bash
$ mkdir envs
$ # create a file named dev in the envs directory with the require environment variables
$ # see dev.env.example
$ ENV=dev make shell
```

Now you are inside a docker container

```
$ make libs
$ make deploy
```

## Test on a device

Inside of the amazon developer portal, create a new skill.

Intents

```json
{
  "intents": [
    {
      "intent": "MyAgeIntent",
        "slots": [
            {
                "name": "dob",
                "type": "AMAZON.DATE"
            }
        ]
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
