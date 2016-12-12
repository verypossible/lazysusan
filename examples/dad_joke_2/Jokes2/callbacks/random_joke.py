import random


def dad_joke(**kwargs):
    paths = (
        "billPath",
        "calendarPath",
        "chickenPath",
        "clydesdalePath",
        "dentistPath",
        "forrestPath",
        "holywaterPath",
        "imDadPath",
        "lifesaversPath",
        "paperPath",
        "peanutsPath",
    )
    return random.choice(paths)
