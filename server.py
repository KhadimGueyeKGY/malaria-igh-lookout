#!/usr/bin/env python3

import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True


class QuieterRequestHandler(SimpleHTTPRequestHandler):
    def send_error(self, code, message=None, explain=None):
        if (
            code == 404
            and ".well-known/appspecific/com.chrome.devtools.json" in self.requestline
        ):
            return
        super().send_error(code, message, explain)

    def log_request(self, code="-", size="-"):
        if str(code) != "200":
            self.log_message('"%s" %s %s', self.requestline, str(code), str(size))


def main():
    port = int(os.environ.get("PORT", 9200))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    url = f"http://localhost:{port}/"

    print(f"Serving at {url}")
    print(f"Directory: {base_dir}")
    print("Press Ctrl+C to stop the server.")

    try:
        webbrowser.open(url)
    except Exception:
        print(f"Could not open browser automatically. Open manually: {url}")

    server_address = ("", port)
    httpd = ThreadedHTTPServer(server_address, QuieterRequestHandler)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()