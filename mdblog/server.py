import os
import shutil
from io import StringIO
from http.server import BaseHTTPRequestHandler, HTTPServer

class Server(HTTPServer):
    def __init__(self, static_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.static_urls = static_urls


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in self.server.static_urls:
            headers, response = self.dispatch_static
            template = "templates/%s.html" % self.path.strip("/")
            with open(template, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                # self.send_header("Content-length", str(len(response)))
                self.end_headers()
                shutil.copyfileobj(f, self.wfile)
