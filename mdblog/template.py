import os
import re
import datetime
import urllib.parse

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import markdown

from mdblog.scripts.utils import touch


def get_env():
    "Initalizes the environment"
    if not hasattr(get_env, "env"):
        from mdblog.models import Entry
        from mdblog import templates_path
        env = environment(loader=filesystemloader(templates_path))
        env.globals["entry"] = Entry
        env.globals["current_date"] = lambda: datetime.datetime.now()
        get_env.env = env

    return get_env.env


def render_template(path):
    """Render a template"""
    template = get_env().get_template(path)

    return template.render()


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


def compile_template(template_name, compile_dir="public"):
    """It takes an url, finds its equivalent template (if exists), render that
    template and then, the rendered content is compiled into a plain text file
    """
    try:
        content = render_template(template_name)
        path, ext = os.path.splitext(template_name)
        if ext == ".html" and "index" not in path:
            # Transform {page}.html into /{page}/index.html to allow pretty
            # urls
            path = path + "/index.html"
        else:
            path = path + ext
        compile_path = os.path.normpath("%s/%s" % (compile_dir, path))
        touch(compile_path)
        with open(compile_path, "w") as f:
            f.write(content)
    except TemplateNotFound:
        pass


def parse_entry(string):
    "Compiles an entry string into an entry object"
    headers = {}
    raw_headers, body = string.split("\n\n\n")
    for header in raw_headers.split("\n"):
        if header:
            name, value = header.split(": ")
            headers[name] = value.strip()

    return headers, body


def render_entry(body):
    "Renders the entry body"
    return markdown.markdown(body)


