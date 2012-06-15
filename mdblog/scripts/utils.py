import os
import re
import argparse
import fnmatch
from functools import wraps


HOST_PORT_REGEXP = re.compile(r"^((\w+):)?(\d{4})$")


def memoize(f):
    "Cache the return value of a function"
    key = "_func_cache"
    @wraps(f)
    def wrapper(*args, **kwargs):
        if hasattr(f, key):
            result = getattr(f, key)
        else:
            result = f(*args, **kwargs)
            setattr(f, key, result)
        return result
    return wrapper


def find_files(start_dir, pattern):
    "Recursively find files matching pattern"
    files = []
    for root, dirnames, filenames in os.walk(start_dir):
        for filename in fnmatch.filter(filenames, pattern):
            files.append(os.path.join(root, filename))

    return files

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


def valid_address(address):
    "Checks if the given string is valid port or host:port pair"
    if not HOST_PORT_REGEXP.match(address):
        msg = "%r is not valid port or host:port pair"
        raise argparse.ArgumentTypeError(msg)
    return address


def parse_address(address):
    "Parse a port or host:port address string and returns the tuple host, port"
    match = HOST_PORT_REGEXP.match(address)
    if match:
        return match.group(2) or "", int(match.group(3))


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


