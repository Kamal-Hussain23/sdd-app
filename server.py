"""The cafe ordering backend server.

A small web server built with Python's built-in tools only. It
holds the menu and orders in memory (there is no database).

Exposes a health check, the menu, and an endpoint to place an order.
"""

import functools
import json
import logging
from collections.abc import Callable
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "0.0.0.0"
PORT = 3000

LOGGER = logging.getLogger("cafe")
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

FRONTEND_HTML = Path(__file__).parent / "frontend" / "index.html"


# ---------------------------------------------------------------------------
# Data models (contracts)
# ---------------------------------------------------------------------------


@dataclass
class Item:
    """A single thing on the menu."""

    name: str
    price: float


@dataclass
class Order:
    """A placed order, kept in memory."""

    order_id: int
    items: list[str]
    status: str


class UnknownItemError(Exception):
    """Raised when an order names an item that is not on the menu."""


class InvalidOrderError(Exception):
    """Raised when an order body is empty or malformed."""


# In-memory data (no database — this resets when the server restarts).
MENU: list[Item] = [
    Item("Latte", 3.5),
    Item("Cappuccino", 3.5),
    Item("Tea", 2.0),
    Item("Croissant", 2.5),
    Item("Muffin", 3.0),
]

ORDERS: list[Order] = []


def _next_order_id() -> int:
    """Return the id to use for the next order."""
    return len(ORDERS) + 1


def place_order(items: list[str]) -> Order:
    """Validate and store a new order, returning it.

    Each item name must be on the menu. The order is kept in memory.
    """
    if not items:
        raise InvalidOrderError("items must not be empty")

    menu_names = {item.name for item in MENU}
    for name in items:
        if name not in menu_names:
            raise UnknownItemError(f"unknown item: {name}")

    order = Order(order_id=_next_order_id(), items=list(items), status="received")
    ORDERS.append(order)
    return order


# ---------------------------------------------------------------------------
# Logging decorator (kept separate from the request-handling logic)
# ---------------------------------------------------------------------------


def log_request(
    method: Callable[["CafeHandler"], None],
) -> Callable[["CafeHandler"], None]:
    """Log each handled request without mixing logging into the logic.

    Wraps a handler method so every request is recorded: when it starts,
    when it finishes, and if it raises an error, the error is logged too.
    """

    @functools.wraps(method)
    def wrapper(self: "CafeHandler") -> None:
        request = f"{self.command} {self.path}"
        LOGGER.info("%s -> start", request)
        try:
            method(self)
        except Exception:
            LOGGER.exception("%s -> error", request)
            raise
        LOGGER.info("%s -> done", request)

    return wrapper


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

    @log_request
    def do_GET(self) -> None:
        """Answer GET requests with a small set of routes."""
        if self.path == "/api/health":
            self._send_json({"status": "ok"})
        elif self.path == "/api/menu":
            self._send_menu()
        elif self.path in ("/", "/index.html"):
            self._send_html(FRONTEND_HTML)
        else:
            self._send_json({"error": "not found"}, status=404)

    @log_request
    def do_POST(self) -> None:
        """Answer POST requests, e.g. placing an order."""
        if self.path == "/api/orders":
            self._place_order()
        else:
            self._send_json({"error": "not found"}, status=404)

    def _send_menu(self) -> None:
        """Send the in-memory menu as JSON."""
        self._send_json({"menu": [{"name": i.name, "price": i.price} for i in MENU]})

    def _place_order(self) -> None:
        """Read the order body, validate and store it, then reply."""
        body = self._read_json_body()
        if body is None:
            self._send_json({"error": "invalid order"}, status=400)
            return

        items = body.get("items")
        if not isinstance(items, list) or not items:
            self._send_json({"error": "invalid order"}, status=400)
            return

        try:
            order = place_order(items)
        except (UnknownItemError, InvalidOrderError) as error:
            self._send_json({"error": str(error)}, status=400)
            return

        self._send_json({"order_id": order.order_id, "status": order.status}, status=201)

    def _read_json_body(self) -> dict[str, object] | None:
        """Read and parse the JSON request body, or None if it is invalid."""
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            body = json.loads(raw)
        except (ValueError, json.JSONDecodeError):
            return None
        if not isinstance(body, dict):
            return None
        return body

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
        """Send the standard access line through our logger instead of stderr."""
        LOGGER.info("access: " + (format % args))


if __name__ == "__main__":
    httpd, _ = make_server()
    print(f"Your site is live at http://localhost:{PORT}/")
    httpd.serve_forever()
