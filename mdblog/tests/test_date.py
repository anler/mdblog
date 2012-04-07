import unittest
import datetime

from mdblog.date import build_date


class BuildDateTest(unittest.TestCase):
    def test_valid_date_string(self):
        "Test that when given a valid date string returns a datetime object"
        date = datetime.datetime(2010, 2, 1, 0, 0)
        date_string = "2010-02-01"
        date_format = "%Y-%m-%d"

        self.assertEqual(date, build_date(date_string, date_format))

    def test_invalid_date_string(self):
        "Test that raises a ValueError if given an invalid date string"
        date_string = "invalid"
        date_format = "%Y-%m-%d"

        self.assertRaises(ValueError, build_date, date_string, date_format)

