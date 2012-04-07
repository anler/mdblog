from http.server import SimpleHTTPRequestHandler, HTTPServer


class Server(HTTPServer):
    pass


class RequestHandler(SimpleHTTPRequestHandler):
    pass
