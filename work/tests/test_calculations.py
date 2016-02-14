import datetime

import pytest


@pytest.fixture
def calculations():
    from work.services import calculations
    return calculations


def test_setup(calculations):
    assert calculations


def test_time_between_happy(calculations):
    start_date = datetime.datetime.now() - datetime.timedelta(days=5)
    end_date = datetime.datetime.now()

    expected = datetime.timedelta(days=5)
    assert calculations.time_between(start_date, end_date).days == expected.days

def test_time_between_unhappy(calculations):
    start_date = datetime.datetime.now()
    end_date = datetime.datetime.now() - datetime.timedelta(days=5)

    with pytest.raises(ValueError) as execinfo:
        calculations.time_between(start_date, end_date)

sunday_data = [
    (
        # Year bounday
        datetime.datetime(2016, 1, 1),
        datetime.datetime(2015, 12, 27)
    ),

    (
        # Leap day
        datetime.datetime(2016, 2, 29),
        datetime.datetime(2016, 2, 28)
    ),

    (
        # Month boundary
        datetime.datetime(2015, 10, 3),
        datetime.datetime(2015, 9, 27)
    ),

    (
        # Sunday
        datetime.datetime(2015, 10, 11),
        datetime.datetime(2015, 10, 11)
    ),

    (
        # Monday
        datetime.datetime(2015, 10, 12),
        datetime.datetime(2015, 10, 11)
    ),

    (
        # Tuesday
        datetime.datetime(2015, 10, 13),
        datetime.datetime(2015, 10, 11)
    ),

    (
        # Wednesday
        datetime.datetime(2015, 10, 14),
        datetime.datetime(2015, 10, 11)
    ),

    (
        # Thursday
        datetime.datetime(2015, 10, 15),
        datetime.datetime(2015, 10, 11)
    ),

    (
        # Friday
        datetime.datetime(2015, 10, 16),
        datetime.datetime(2015, 10, 11)
    ),

    (
        # Saturday
        datetime.datetime(2015, 10, 17),
        datetime.datetime(2015, 10, 11)
    ),
]
@pytest.mark.parametrize("input,expected", sunday_data)
def test_sunday(calculations, input, expected):
    actual = calculations.sunday_of_week(input)
    assert actual.year == expected.year
    assert actual.month == expected.month
    assert actual.day == expected.day
