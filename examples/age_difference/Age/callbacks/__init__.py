import random

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from lazysusan.logger import get_logger
from lazysusan.helpers import build_response
from lazysusan.response import build_response_payload


DOB_KEY = "LAST_DOB"
YEAR = timedelta(days=365)


def get_dob_from_date_string(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return None


def get_age_from_dob(dob, now=None):
    now = now or datetime.now()
    return relativedelta(now, dob)


def is_leap_day(date):
    return date.month == 2 and date.day == 29


def is_leap_year(year):
    # allow for passing of datetimes
    if hasattr(year, 'year'):
        year = year.year

    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        return True
    return False


def is_birthday(dob, now):
    if not is_leap_day(dob):
        return dob.month == now.month and dob.day == now.day

    # user's bday is on feb 29
    if is_leap_year(now):
        return is_leap_day(now)
    else:
        return now.month == 2 and now.day == 28


def is_valid_day(dob):
    """Validate whether a given day is valid

    Mainly checks whether a leap day is valid for a given year. Ie, Feb 29, 1997 isn't a valid day.

    """
    if not dob:
        return False

    if dob.month == 2 and dob.day == 29:
        return is_leap_year(dob.year)

    return True


def _handle_days_until_bday(dob, now):
    next_bday = datetime(now.year + 1, dob.month or 0, dob.day or 0)

    is_birthday_this_year = True if next_bday - now > YEAR else False
    if is_birthday_this_year:
        next_bday = datetime(now.year, dob.month, dob.day)

    delta = next_bday - now
    return delta.days


def _handle_leap_days_until_bday(dob, now):
    assert is_leap_year(dob.year)

    # See if it's the leap year users bday
    if (not is_leap_year(now) and now.month == 2 and now.day == 28) or \
            (is_leap_year(now) and is_leap_day(now)):
        return 0

    dob_day_this_year = 29 if is_leap_year(now.year) else 28
    dob_day_next_year = 29 if is_leap_year(now.year + 1) else 28

    next_bday = datetime(now.year + 1, 2, dob_day_next_year)

    is_birthday_this_year = True if next_bday - now > YEAR else False
    if is_birthday_this_year:
        next_bday = datetime(now.year, dob.month, dob_day_this_year)

    delta = next_bday - now
    return delta.days


def days_until_birthday(dob, now):
    """Return a string stating the number of days until next birthday.

    :param dob: A person's date of birth
    :type dob: datetime object
    :param now: The current date and time to base the calculation on
    :type dob: datetime object

    """
    if is_birthday(dob, now):
        return ""

    # be careful b/c leap years need to be handled differently if somone's birthday is on leap day
    if not is_leap_day(dob):
        days_to_bday = _handle_days_until_bday(dob, now)
    else:
        days_to_bday = _handle_leap_days_until_bday(dob, now)

    return "It's %s days until your next birthday.  " % (days_to_bday, )


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


def calc_difference(**kwargs):
    request = kwargs["request"]
    session = kwargs["session"]
    state_machine = kwargs["state_machine"]
    log = get_logger()

    date_string = request.get_slot_value("dob")
    if not date_string:
        log.error("Could not find date in slots")
        return "goodBye"

    if date_string.startswith('XXXX-'):
        return "missingYear"

    now = datetime.now()

    dob = get_dob_from_date_string(date_string)
    if not is_valid_day(dob):
        return "invalidDate"

    age = get_age_from_dob(dob, now)

    # First get a breakdown of how old user is in years, months, days
    msg = age_breakdown(age)

    # next figure out the days until the users next birthday
    msg += "%s" % (days_until_birthday(dob, now), )

    # finally add whether we're older or younger than the last user
    msg += "%s" % (last_user_difference(session, dob), )

    session.set(DOB_KEY, dob.toordinal())

    response_dict = build_response("ageResponse", msg, state_machine)
    return build_response_payload(response_dict, session.get_state_params())
