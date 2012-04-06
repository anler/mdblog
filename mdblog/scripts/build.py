"""
Render templates and build the blog
"""
import sys
import os
import glob
import argparse

from mdblog.template import compile_url_template
from mdblog.parse import extract_links


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)

    templates = {t for t in glob.glob("templates/*.html")}
    for template_name in templates:
        print("Extracting template %r links" % template_name)
        with open(template_name) as t:
            links = extract_links(t.read())
        if links:
            print("%i links found" % len(links))
            for url in links:
                template_name = url_to_template(url)
                compile_template(template_name)
        else:
            print("No links found")
    # Compile index.html manually
    compile_template("index.html")
