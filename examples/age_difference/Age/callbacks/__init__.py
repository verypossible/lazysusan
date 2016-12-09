import random

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from lazysusan.logger import get_logger
from lazysusan.helpers import (
    build_response,
    get_slot_value,
)
from lazysusan.response import build_response_payload


DOB_KEY = "LAST_DOB"
YEAR = timedelta(days=365)


def calc_difference(**kwargs):
    request = kwargs["request"]
    session = kwargs["session"]
    state_machine = kwargs["state_machine"]
    log = get_logger()

    date_string = get_slot_value(request, "dob")
    if not date_string:
        log.error("Could  not find date in slots")
        return "goodBye"

    now = datetime.now()

    dob = get_dob_from_date_string(date_string)
    age = get_age_from_date_string(dob, now)

    # First get a breakdown of how old user is in years, months, days
    msg = age_breakdown(age)

    # next figure out the days until the users next birthday
    msg += "%s" % (days_until_birthday(dob, now), )

    # finally add whether we're older or younger than the last user
    msg += "%s" % (last_user_difference(session, dob), )

    session.set(DOB_KEY, dob.toordinal())

    response_dict = build_response("ageResponse", msg, state_machine)
    return build_response_payload(response_dict, session.get_state_params())


def get_dob_from_date_string(date_string):
    return datetime.strptime(date_string, "%Y-%m-%d")


def get_age_from_dob(dob, now=None):
    now = now or datetime.now()
    return relativedelta(now, dob)

def is_birthday(dob, now):
    return dob.month == now.month and dob.day == now.day


def days_until_birthday(dob, now):
    """Return a string stating the number of days until next birthday.

    :param dob: A person's date of birth
    :type dob: datetime object
    :param now: The current date and time to base the calculation on
    :type dob: datetime object

    """
    if is_birthday(dob, now):
        return ""

    next_bday = datetime(now.year + 1, dob.month or 0, dob.day or 0)

    is_birthday_this_year = True if next_bday - now >= YEAR else False
    if is_birthday_this_year:
        next_bday = datetime(now.year, dob.month, dob.day)

    delta = next_bday - now
    days_to_bday = delta.days
    if days_to_bday:
        return "It's %s days until your next birthday.  " % (days_to_bday, )
    else:
        return " "


def age_breakdown(age):
    if not age.months and not age.days:
        return "Happy birthday! You are %s years old today. " % (age.years, )

    msg = ["You are %s years" % (age.years, )]

    if age.months > 0:
        if age.months == 1:
            msg.append("one month")
        else:
            msg.append("%s months, " % (age.months, ))

    if age.days > 0:
        if age.days == 1:
            msg.append("one day old")
        else:
            msg.append("%s days old" % (age.days, ))

    return ", ".join(msg) + ".  "


def last_user_difference(session, dob):
    last_date = session.get(DOB_KEY)
    if not last_date:
        return ''

    last_date = datetime.fromordinal(last_date)
    old_or_younger = "same"

    if dob > last_date:
        old_or_younger = "younger"
        diff = relativedelta(dob, last_date)
    elif dob < last_date:
        old_or_younger = "older"
        diff = relativedelta(last_date, dob)

    if old_or_younger != "same":
        return "You are %s years, %s months, %s days %s than the last user." % (
                diff.years, diff.months, diff.days, old_or_younger)

    return "You have the same birthday as the last user."
