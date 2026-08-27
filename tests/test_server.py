"""Tests for the cafe ordering backend server."""

import json
import logging
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from typing import cast

import pytest

import server

OK = 200
CREATED = 201
BAD_REQUEST = 400


@pytest.fixture()
def server_url() -> Iterator[str]:
    """Start the server on a free port for the test, then stop it."""
    httpd, port = server.make_server(port=0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()


@pytest.fixture()
def clean_orders() -> Iterator[None]:
    """Empty the in-memory orders before each test so ids are predictable."""
    server.ORDERS.clear()
    yield


def post_json(url: str, payload: object) -> tuple[int, dict[str, object]]:
    """POST a JSON payload and return (status_code, parsed_body)."""
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, json.load(error)


def test_health_returns_ok(server_url: str) -> None:
    """The health endpoint reports the server is up."""
    with urllib.request.urlopen(f"{server_url}/api/health") as response:
        assert response.status == OK
        body = json.load(response)
    assert body == {"status": "ok"}


def test_requests_are_logged(server_url: str, caplog: pytest.LogCaptureFixture) -> None:
    """Each handled request is logged with its method and path."""
    with (
        caplog.at_level(logging.INFO, logger=server.LOGGER.name),
        urllib.request.urlopen(f"{server_url}/api/health") as response,
    ):
        assert response.status == OK

    messages = [r.getMessage() for r in caplog.records]
    assert any("GET /api/health" in m for m in messages)


def test_menu_endpoint_returns_menu(server_url: str) -> None:
    """GET /api/menu returns the in-memory menu with name and price."""
    with urllib.request.urlopen(f"{server_url}/api/menu") as response:
        assert response.status == OK
        body = json.load(response)
    assert "menu" in body
    assert len(body["menu"]) == len(server.MENU)
    for item in body["menu"]:
        assert "name" in item and "price" in item


def test_place_order_endpoint_success(server_url: str, clean_orders: None) -> None:
    """A valid order is stored and returns 201 with an order id."""
    status, body = post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    assert status == CREATED
    assert body["status"] == "received"
    assert body["order_id"] == 1
    assert len(server.ORDERS) == 1


def test_place_order_endpoint_ids_increment(server_url: str, clean_orders: None) -> None:
    """Two orders get increasing ids through the endpoint."""
    _, first = post_json(f"{server_url}/api/orders", {"items": ["Latte"]})
    _, second = post_json(f"{server_url}/api/orders", {"items": ["Tea"]})
    assert cast(int, second["order_id"]) == cast(int, first["order_id"]) + 1


def test_place_order_unknown_item_rejected(server_url: str, clean_orders: None) -> None:
    """An item not on the menu returns 400 and nothing is stored."""
    status, body = post_json(f"{server_url}/api/orders", {"items": ["Not On The Menu"]})
    assert status == BAD_REQUEST
    assert "error" in body
    assert len(server.ORDERS) == 0


def test_place_order_empty_rejected(server_url: str, clean_orders: None) -> None:
    """An empty items list returns 400 and nothing is stored."""
    status, body = post_json(f"{server_url}/api/orders", {"items": []})
    assert status == BAD_REQUEST
    assert "error" in body
    assert len(server.ORDERS) == 0


def test_place_order_missing_items_key_rejected(server_url: str, clean_orders: None) -> None:
    """A body without the 'items' key returns 400."""
    status, body = post_json(f"{server_url}/api/orders", {"menu": ["Latte"]})
    assert status == BAD_REQUEST
    assert "error" in body


def test_place_order_non_list_items_rejected(server_url: str, clean_orders: None) -> None:
    """A body where 'items' is not a list returns 400."""
    status, body = post_json(f"{server_url}/api/orders", {"items": "Latte"})
    assert status == BAD_REQUEST
    assert "error" in body
