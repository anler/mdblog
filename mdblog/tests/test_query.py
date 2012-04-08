import unittest

from mdblog.query import entry_string_to_dict, filename_to_slug


class EntryStringToDictTest(unittest.TestCase):
    def test(self):
        "Test that returns a dictionary equivalent to the pased entry string"
        entry_string = "title: Entry title  \n\n\n# Entry body"
        entry_dict = entry_string_to_dict(entry_string)
        self.assertEqual("Entry title", entry_dict["title"])
        self.assertEqual("<h1>Entry body</h1>", entry_dict["body"])


class FilenameToSlugTest(unittest.TestCase):
    def test(self):
        "Test that returns a slug computed from the filename"
        filename = "dynamic_site/path/to/entry-name.md"
        self.assertEqual("/path/to/entry-name/", filename_to_slug(filename))
