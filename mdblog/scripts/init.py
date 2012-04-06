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

    mktree("%s/entries" % project_name)
    mktree("%s/snippets" % project_name)

    touch("%s/templates/base.html" % project_name)
    touch("%s/templates/index.html" % project_name)
    touch("%s/templates/entry.html" % project_name)
    touch("%s/templates/snippet.html" % project_name)
    touch("%s/templates/tag.html" % project_name)

