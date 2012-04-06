import unittest

from mdblog.template import url_to_template


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


