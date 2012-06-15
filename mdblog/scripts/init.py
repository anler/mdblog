"""
Creates the blog's base structure of files and directories
"""
import sys
import shutil
import argparse

from mdblog import templates_path
from mdblog.scripts.utils import valid_name, touch


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("name", type=valid_name, help="Your blog's name")

    args = parser.parse_args(argv)

    project_name = args.name

    touch("%s/%s/base.html" % (project_name, templates_path))
    touch("%s/%s/index.html" % (project_name, templates_path))


if __name__ == "__main__":
    main()
