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

def calc_difference(request, session, intent, context, user_id, state_machine):
    log = get_logger()

    date = get_slot_value(request, "dob")
    if not date:
        log.error("Could  not find date in slots")
        return "goodBye"

    log.info("Got date from slots: %s" % (date, ))

    now = datetime.now()

    dob = datetime.strptime(date, "%Y-%m-%d")
    age = relativedelta(now, dob)

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

    last_date = session.get(DOB_KEY)
    if last_date:
        last_date = datetime.fromordinal(last_date)
        diff = relativedelta(dob, last_date)
        old_or_younger = 'younger' if dob < last_date else 'older'
        msg += '. You are %s years, %s months, %s days %s than the last user.' % (
                diff.years, diff.months, diff.days, old_or_younger)

    session.set(DOB_KEY, dob.toordinal())

    response_dict = build_response("ageResponse", msg, state_machine)
    return build_response_payload(response_dict, session.get_state_params())
