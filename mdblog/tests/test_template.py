import datetime
import unittest

from mdblog.template import url_to_template, render_entry, parse_entry


class UrlToTemplateTest(unittest.TestCase):
    def test_absolute_url(self):
        url = "http://domain.com/path/subpath/"
        self.assertEqual("/path/subpath.html", url_to_template(url))

    def test_absolute_resource(self):
        url = "http://domain.com/path/subpath/style.css"
        self.assertEqual("/path/subpath/style.css", url_to_template(url))

    def test_absolute_url_without_trailing_slash(self):
        url = "http://domain.com/path/subpath"
        self.assertEqual("/path/subpath.html", url_to_template(url))

    def test_relative_url(self):
        url = "/path/subpath/"
        self.assertEqual("/path/subpath.html", url_to_template(url))

    def test_relative_resource(self):
        url = "/path/subpath/style.css"
        self.assertEqual("/path/subpath/style.css", url_to_template(url))

    def test_relative_url_without_trailing_slash(self):
        url = "/path/subpath"
        self.assertEqual("/path/subpath.html", url_to_template(url))

    def test_relative_url_without_begining_slash(self):
        url = "path/subpath"
        self.assertEqual("path/subpath.html", url_to_template(url))


class ParseEntryTest(unittest.TestCase):
    def test_parse(self):
        "Test that parses the entry text correctly"
        entry = "title: Entry title  \ndate: 2012-02-12  \n"\
                "\n\n# This is the entry"
        headers, body = parse_entry(entry)

        self.assertEqual("Entry title", headers["title"])
        self.assertEqual("2012-02-12", headers["date"])
        self.assertEqual("# This is the entry", body)


class RenderEntryTest(unittest.TestCase):
    def test_render(self):
        "Test that a text entry is rendered and compiled into an Entry object"
        body = render_entry("# This is the entry")

        self.assertEqual("<h1>This is the entry</h1>", body)

