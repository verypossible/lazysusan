from datetime import datetime
from dateutil.relativedelta import relativedelta

import pytest

from callbacks import (
    get_dob_from_date_string,
    get_age_from_dob,
    days_until_birthday,
    is_leap_year,
)

leap_years = set((
    1904, 1908, 1912, 1916, 1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960,
    1964, 1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020,
    2024, 2028, 2032, 2036, 2040
))
regular_years = (i for i in xrange(1900, 2040) if i not in leap_years)


@pytest.mark.parametrize("year", leap_years)
def test_is_leap_year(year):
    assert is_leap_year(year) is True


@pytest.mark.parametrize("year", regular_years)
def test_is_not_leap_year(year):
    assert is_leap_year(year) is False


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
    # random
    (datetime(1973, 4, 20), datetime(2016, 12, 9), 132),
    # leap year
    (datetime(1994, 12, 31), datetime(2016, 1, 1), 365),
    # regular year
    (datetime(1994, 12, 31), datetime(2017, 1, 1), 364),
    # birthday
    (datetime(1994, 12, 31), datetime(2016, 12, 31), ""),
    # one day away on borders
    (datetime(1937, 1, 1), datetime(2016, 12, 31), 1),
    # thi year not a leap year but next year is
    (datetime(1960, 2, 29), datetime(2015, 2, 27), 1),
    (datetime(1960, 2, 29), datetime(2015, 2, 28), ""),
    (datetime(1960, 2, 29), datetime(2015, 3, 1), 365),
    # this year is a leap year
    (datetime(1960, 2, 29), datetime(2016, 2, 27), 2),
    (datetime(1960, 2, 29), datetime(2016, 2, 28), 1),
    (datetime(1960, 2, 29), datetime(2016, 2, 29), ""),
    (datetime(1960, 2, 29), datetime(2016, 3, 1), 364),
    # this year and next year not leap years
    (datetime(1960, 2, 29), datetime(2017, 2, 27), 1),
    (datetime(1960, 2, 29), datetime(2017, 2, 28), ""),
    (datetime(1960, 2, 29), datetime(2017, 3, 1), 364),
)

@pytest.mark.parametrize("dob, now, expected", days_til_bday_data)
def test_days_until_birthday(dob, now, expected):
    if expected:
        expected = "It's %s days until your next birthday." % (expected, )
    assert expected == days_until_birthday(dob, now).strip()
