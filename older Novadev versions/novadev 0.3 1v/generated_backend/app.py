"""Generated NovaDev 0.3 backend app.

Run with:
    python app.py
Then open http://127.0.0.1:8000/api/products or another generated route.
"""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from routes import handle_route


class NovaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond("GET")

    def do_POST(self):
        self.respond("POST")

    def respond(self, method):
        path = urlparse(self.path).path
        result, status = handle_route(method, path)
        payload = json.dumps(result).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), NovaHandler)
    print("NovaDev backend running at http://127.0.0.1:8000")
    server.serve_forever()
