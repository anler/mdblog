"""
Creates the blog scaffold
"""
import sys
import shutil
import argparse

from mdblog.scripts.utils import valid_name, mktree, touch


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", type=valid_name, help="Your blog's name")

    args = parser.parse_args(argv)

    project_name = args.name

    touch("%s/dynamic_site/base.html" % project_name)
    touch("%s/dynamic_site/index.html" % project_name)

