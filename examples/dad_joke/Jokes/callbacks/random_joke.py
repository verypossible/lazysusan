import random


def dad_joke(request, state_machine):
    paths = (
        "chickenPath",
        "clydesdalePath",
        "dentistPath",
        "lifesaversPath",
    )
    return random.choice(paths)
