"""
Runs a lightweight webserver used for development and that it is reloaded
every time a file in the root directory is changed.
"""
import sys
import os
import re
import time
import signal
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler

from mdblog.scripts.utils import is_dir, valid_address, parse_address


def run(root, address):
    """Runs a simple web server at address using root as the directory root"""
    print("Ready to rumble at %s:%s" % address)
    print("Root directory is: %s" % root)
    os.chdir(root)
    httpd = HTTPServer(address, SimpleHTTPRequestHandler)
    httpd.serve_forever()


def watch(directory, channel):
    """Watches changes in any file in the given directory"""
    hidd_re = re.compile(r"^\.")

    def _get_mtimes():
        mtimes = 0
        for dirpath, dirname, filenames in os.walk(directory):
            mtimes += sum(os.stat(os.path.join(dirpath, f)).st_mtime
                          for f in filenames if not hidd_re.match(f))
        return mtimes

    mtimes = _get_mtimes()
    while True:
        last_mtimes = _get_mtimes()
        if mtimes < last_mtimes:
            os.write(channel, b"reload\n")
            mtimes = last_mtimes
        time.sleep(1)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-a", "--address", dest="address", type=valid_address,
                        help="The port or host:port pair at which run server")
    parser.add_argument("-r", "--root-directory", type=is_dir, default=".",
                        help="The root directory. Defaults to current.")
    args = parser.parse_args(argv)

    if args.address:
        address = parse_address(args.address)
    else:
        address = ("", 3000)
    root = os.path.abspath(args.root_directory)

    def _spawn_http_server():
        http_child = os.fork()
        if http_child == 0:
            run(root, address)
            os._exit(0)
        else:
            return http_child

    http_child = _spawn_http_server()
    ch_read, ch_write = os.pipe()
    watch_child = os.fork()
    if watch_child == 0:
        os.close(ch_read)
        watch(root, channel=ch_write)
        os._exit(0)

    os.close(ch_write)
    channel = os.fdopen(ch_read)
    while True:
        command = channel.readline()
        if "reload" in command:
            print("Change detected, reloading http server...")
            os.kill(http_child, signal.SIGTERM)
            try:
                os.wait()
            except OSError:
                pass
            http_child = _spawn_http_server()
        time.sleep(1)


if __name__ == "__main__":
    main()
