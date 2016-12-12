import random

from datetime import datetime
from dateutil.relativedelta import relativedelta

from lazysusan.logger import get_logger
from lazysusan.helpers import (
    build_response,
    get_slot_value,
)
from lazysusan.response import build_response_payload


DOB_KEY = "LAST_DOB"

def calc_difference(**kwargs):
    request = kwargs["request"]
    session = kwargs["session"]
    state_machine = kwargs["state_machine"]
    log = get_logger()

    date = request.get_slot_value("dob")
    if not date:
        log.error("Could  not find date in slots")
        return "goodBye"

    log.info("Got date from slots: %s" % (date, ))

    now = datetime.now()

    dob = datetime.strptime(date, "%Y-%m-%d")
    age = relativedelta(now, dob)

    msg = age_breakdown(age)
    msg += ". %s" % (last_user_difference(session, dob))

    session.set(DOB_KEY, dob.toordinal())

    response_dict = build_response("ageResponse", msg, state_machine)
    return build_response_payload(response_dict, session.get_state_params())


def age_breakdown(age):
    if not age.months and not age.days:
        msg = "Happy birthday! You are %s years old today" % (age.years, )
    else:
        msg = "You are %s years, " % (age.years, )
        if age.months > 0:
            if age.months == 1:
                msg += "one month, "
            else:
                msg += "%s months, " % (age.months, )

        if age.days > 0:
            if age.days == 1:
                msg += "one day old"
            else:
                msg += "%s days old" % (age.days, )
    return msg


def last_user_difference(session, dob):
    last_date = session.get(DOB_KEY)
    if last_date:
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
