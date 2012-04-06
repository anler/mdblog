import unittest

from mdblog.parse import extract_links


class ExtractLinksTest(unittest.TestCase):
    def test_without_relative(self):
        "Tests that an empty list is returned if no relative links are found"
        template = """\
        <html>
            <head>
                <link href="http://url/style.css">
            </head>
            <body>
                <a href="http://some-url/">Link</a>
            </body>
        </html>
        """
        self.assertEqual({"http://url/style.css", "http://some-url/"},
                         extract_links(template))

    def test_with_relative(self):
        "Tests that a list is returned with relative links found"
        template = """\
        <html>
            <head>
                <link href="/style.css">
            </head>
            <body>
                <a href="/some-url/">Link</a>
            </body>
        </html>
        """
        self.assertEqual({"/style.css", "/some-url/"}, extract_links(template))
