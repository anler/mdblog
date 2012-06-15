"""
Render all templates stored in `dynamic_site` directory and compiles the result
as html files in `public` directory.
"""
import sys
import os
import glob
import argparse

from mdblog import templates_path, compile_dir
from mdblog.models import Entry, Snippet
from mdblog.template import compile_template, url_to_template
from mdblog.parse import extract_links


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    args = parser.parse_args(argv)

    templates = {t for t in glob.glob("%s/*.html" % templates_path)}
    for template_name in templates:
        print("Extracting template %r links" % template_name)
        with open(template_name) as t:
            links = extract_links(t.read())
        if links:
            print("%i links found" % len(links))
            for url in links:
                template_name = url_to_template(url)
                path, ext = os.path.splitext(template_name)
                if ext == ".html":
                    # Transform path/to/page.html into path/to/page/index.html
                    path = path + "/index.html"
                else:
                    path += ext
                output = compile_dir + path
                compile_template(template_name, output)
        else:
            print("No links found")
    output = compile_dir + "/index.html"
    compile_template("index.html", output)
    for entry in Entry.objects.all():
        output = compile_dir + entry.slug + "index.html"
        compile_template("entry.html", output, context={"entry": entry})
    for snippet in Snippet.objects.all():
        output = compile_dir + snippet.slug + "index.html"
        compile_template("snippet.html", output, context={"snippet": snippet})


if __name__ == "__main__":
    main()
