from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytest

from callbacks import (
    get_dob_from_date_string,
    get_age_from_dob,
    days_until_birthday,
)

get_dt_data = (
    ("1995-01-01", datetime(1995, 1, 1)),
    ("2001-12-15", datetime(2001, 12, 15)),
    ("1973-04-20", datetime(1973, 4, 20)),
    ("1960-02-29", datetime(1960, 2, 29)),
)

@pytest.mark.parametrize("datestring, expected", get_dt_data)
def test_dt_from_string(datestring, expected):
    assert expected == get_dob_from_date_string(datestring)


get_age_data = (
    (datetime(1995, 1, 1), datetime(2016, 1, 1), relativedelta(years=21)),
    (datetime(2001, 12, 15), datetime(2017, 12, 15), relativedelta(years=16)),
    (datetime(1973, 4, 20), datetime(2016, 12, 9), relativedelta(years=43, months=7, days=19) ),
    (datetime(1960, 2, 29), datetime(2017, 3, 1), relativedelta(years=57, days=1) ),
)

@pytest.mark.parametrize("dob, now, expected", get_age_data)
def test_get_age_from_date_string(dob, now, expected):
    assert expected == get_age_from_dob(dob, now)


days_til_bday_data = (
    (datetime(1973, 4, 20), datetime(2016, 12, 9), 132),
    (datetime(1994, 12, 31), datetime(2017, 1, 1), 364),
    (datetime(1994, 12, 31), datetime(2016, 12, 31), ""),
    (datetime(1937, 1, 1), datetime(2016, 12, 31), 1),
    (datetime(1960, 2, 29), datetime(2016, 4, 1), 1),
    #(datetime(1960, 2, 29), datetime(2020, 3, 1), 1),
    # (datetime(2016, 12, 9), 55 ),
    # (datetime(2017, 3, 1), 55),
)

@pytest.mark.parametrize("dob, now, expected", days_til_bday_data)
def test_days_until_birthday(dob, now, expected):
    if expected:
        expected = "It's %s days until your next birthday." % (expected, )
    assert expected == days_until_birthday(dob, now).strip()
