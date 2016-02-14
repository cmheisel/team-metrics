"""
Functions for doing calculations on/about work objects.
"""
import datetime


def time_between(start_date, end_date):
    if end_date < start_date:
        raise ValueError("Start must pre-date end: {} < {}".format(end_date, start_date))
    return end_date - start_date


def sunday_of_week(target_date):
    if target_date.weekday() == 6:
        return datetime.date(target_date.year, target_date.month, target_date.day)
    return sunday_of_week(target_date - datetime.timedelta(days=1))
