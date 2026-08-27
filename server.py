"""The cafe ordering backend server.

A small web server built with Python's built-in tools only. It
holds the menu and orders in memory (there is no database).

For now it exposes a single health check endpoint so we can prove
the server runs and talks to the frontend.
"""

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 3000

FRONTEND_HTML = Path(__file__).parent / "frontend" / "index.html"


def make_server(port: int = PORT) -> tuple[ThreadingHTTPServer, int]:
    """Create the server on the given port and return it with the port.

    If port is 0, the OS picks a free one; we return the real port so
    the caller knows where to connect.
    """
    httpd = ThreadingHTTPServer((HOST, port), CafeHandler)
    actual_port = httpd.server_address[1]
    return httpd, actual_port


class CafeHandler(BaseHTTPRequestHandler):
    """Handles one web request at a time."""

    def do_GET(self) -> None:
        """Answer GET requests with a small set of routes."""
        if self.path == "/api/health":
            self._send_json({"status": "ok"})
        elif self.path in ("/", "/index.html"):
            self._send_html(FRONTEND_HTML)
        else:
            self._send_json({"error": "not found"}, status=404)

    def _send_json(self, data: dict[str, object], status: int = 200) -> None:
        """Send a Python dict back to the browser as JSON."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, path: Path) -> None:
        """Send an HTML file back to the browser."""
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        """Keep the console quiet during tests."""
        return


if __name__ == "__main__":
    httpd, _ = make_server()
    print(f"Your site is live at http://localhost:{PORT}/")
    httpd.serve_forever()
