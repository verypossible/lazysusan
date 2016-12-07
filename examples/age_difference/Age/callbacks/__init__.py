import random

from datetime import datetime
from dateutil.relativedelta import relativedelta

from lazysusan.logger import get_logger
from lazysusan.response import build_response_payload


def calc_difference(request, session, intent, context, user_id, state_machine):
    log = get_logger()
    # get the date
    try:
        date = request["intent"]["slots"]["dob"]["value"]
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

        response = state_machine["ageResponse"]["response"]
        response["outputSpeech"]["text"] = msg
        return build_response_payload(response, session.get_state_params())
    except (KeyError, TypeError):
        date = ""
        log.error("Could  not find date in slots")

    return "goodBye"
