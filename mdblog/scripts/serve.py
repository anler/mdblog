"""
Serves site blog dynamically. Used when developing the site.
"""
import sys
import argparse

from mdblog.server import Server, RequestHandler


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=is_dir, help="Server root")
    parser.add_argument("-h", "--host", default="",
                        help="Server host. Defaults to localhost")
    parser.add_argument("-p", "--port", default="3030", type=int,
                        help="Server port. Defaults to 3030")
    args = parser.parse_args(argv)

    address = ("", args.port)

    server = Server(address, RequestHandler)
    server.serve_forever()

