import os
import fnmatch

from mdblog import templates_path
from mdblog.template import render_entry, parse_entry
from mdblog.scripts.utils import find_files


def entry_string_to_dict(entry_string):
    "Returns a dictionary with the attributes of an entry parsed from a string"
    headers, body = parse_entry(entry_string)
    entry_dict = {
        "body": render_entry(body)
    }
    entry_dict.update(headers)

    return entry_dict


def filename_to_slug(filename):
    "Returns a slug computed from the filename"
    slug, ext = os.path.splitext(filename.replace(templates_path, ""))
    return "/%s/" % slug.strip("/")


def find_md_templates(pattern):
    "Find markdown templates matching a pattern"
    def finder():
        entries = []
        for filename in find_files(templates_path, pattern):
            with open(filename) as raw_entry:
                entry_dict = entry_string_to_dict(raw_entry.read())
                entry_dict.update({
                    "slug": filename_to_slug(filename)
                })
                entries.append(entry_dict)

        return entries
    return finder
