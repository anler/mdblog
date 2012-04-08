import datetime
import unittest

from mdblog.models import Entry, Manager


class EntryTest(unittest.TestCase):
    def test_attributes_creation(self):
        "Test that an Entry is created with the attrs passed as kwargs"
        attrs = {
            "title": "Entry title",
            "slug": "entry-title",
            "date": "2010-02-01",
            "excerpt": "Entry excerpt",
            "body": "Entry body",
        }
        entry = Entry(**attrs)

        self.assertEqual(attrs["title"], entry.title)
        self.assertEqual(attrs["slug"], entry.slug)
        self.assertIsInstance(entry.date, datetime.datetime)
        self.assertEqual(attrs["excerpt"], entry.excerpt)
        self.assertEqual(attrs["body"], entry.body)


class ManagerTest(unittest.TestCase):
    def setUp(self):
        entries = [
            dict(title="Entry 1", date="2010-2-1"),
            dict(title="Entry 2", date="2011-2-1"),
            dict(title="Entry 3", date="2009-2-1")
        ]
        self.query = lambda: entries

    def test_latest_entry(self):
        "Test that latest() returns the more recent entry"
        latest, = Manager(query=self.query).latest()

        self.assertEqual("Entry 2", latest.title)

    def test_latest(self):
        "Test that latest(n) returns the n more recent entries"
        latest = Manager(query=self.query).latest(3)

        self.assertEqual("Entry 2", latest[0].title)
        self.assertEqual("Entry 1", latest[1].title)
        self.assertEqual("Entry 3", latest[2].title)

    def test_all(self):
        "Test that latest() returns all the entries ordered by date"
        self.assertEqual(3, len(Manager(query=self.query).all()))

