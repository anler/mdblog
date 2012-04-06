"""
Serves site blog dynamically. Used when developing the site.
"""
import sys
import glob
import argparse

from mdblog.urls import add_path
from mdblog.server import Server, RequestHandler
from mdblog.parse import extract_links
from mdblog.scripts.utils import is_dir


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("templates_path", type=is_dir, help="Path to templates")
    parser.add_argument("-p", "--port", default="3030", type=int,
                        help="Server port. Defaults to 3030")
    args = parser.parse_args(argv)

    address = ("", args.port)
    templates = "%s/*.html" % args.templates_path
    static_urls = []

    for template in glob.glob(templates):
        static_urls += extract_links(open(template).read())

    server = Server(static_urls, address, RequestHandler)
    server.serve_forever()

