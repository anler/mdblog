import os
import re
import datetime
import urllib.parse

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import markdown

from mdblog.date import rfc3339
from mdblog.scripts.utils import touch, memoize


@memoize
def get_env():
    "Initalizes the environment"
    from mdblog.models import Entry, Snippet
    from mdblog import templates_path

    env = Environment(loader=FileSystemLoader(templates_path))
    env.globals["Entry"] = Entry
    env.globals["Snippet"] = Snippet
    env.globals["current_date"] = datetime.datetime.utcnow
    env.globals["rfc3339"] = rfc3339

    return env


def render_template(path, context):
    """Render a template"""
    template = get_env().get_template(path)

    return template.render(context)


def url_to_template(url):
    "Translates the given url into a filesystem path"
    components = urllib.parse.urlparse(url)
    if components.path:
        path = components.path
    else:
        path = "home.html"
    if not re.search(r"[\w-]+\.[\w\-]+$", path):
        if path.endswith("/"):
            path = path[:-1]
        path += ".html"

    return path


def compile_template(template_name, output, context={}):
    """It takes a tempate name, renders that template and the rendered content
    is compiled into a plain text file inside output
    """
    try:
        content = render_template(template_name, context)
        touch(output)
        with open(output, "w") as f:
            f.write(content)
    except TemplateNotFound:
        pass


def parse_entry(string):
    "Compiles an entry string into an entry object"
    headers = {}
    raw_headers, body = string.split("\n\n\n", 1)
    for header in raw_headers.split("\n"):
        if header:
            name, value = header.split(": ")
            headers[name] = value.strip()

    return headers, body


def render_entry(body):
    "Renders the entry body"
    return markdown.markdown(body)


