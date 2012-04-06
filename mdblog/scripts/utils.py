import os
import re
import argparse


def is_dir(path):
    "Checks if path is a valid directory"
    if not os.path.isdir(path):
        msg = "%r is not an existing directory" % path
        raise argparse.ArgumentTypeError(msg)

    return path


def valid_name(name):
    "Checks if the given name is a valid project name"
    if not re.match(r"^\w+$", name):
        msg = "%r is not a valid project name. Use letters, numbers and "\
              "underscores only" % name
        raise argparse.ArgumentTypeError(msg)

    if os.path.isdir(name):
        msg = "%r is an existing directory" % name
        raise argparse.ArgumentTypeError(msg)

    return name


def mktree(path):
    "Recursively creates the given directory tree"
    os.makedirs(path, exist_ok=True)


def touch(path):
    "Creates an empty file"
    head, tail = os.path.split(path)
    if head:
        mktree(head)
    with open(path, "w") as f:
        f.write("")


