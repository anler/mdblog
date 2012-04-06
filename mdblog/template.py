import os
import re
import urllib.parse

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from mdblog.entries import get_recent_entries
from mdblog.scripts.utils import touch

env = Environment(loader=FileSystemLoader("templates"))
env.globals["get_recent_entries"] = get_recent_entries


def render_template(path):
    """Render a template"""
    template = env.get_template(path)

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


