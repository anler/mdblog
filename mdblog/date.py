import time
import datetime


def build_date(date_string, date_format):
    """Build a datetime object from a date_string with date_format"""
    return datetime.datetime.fromtimestamp(time.mktime(
        time.strptime(date_string, date_format)))
