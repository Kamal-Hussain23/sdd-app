"""Tests for the cafe ordering backend server."""

import json
import threading
import urllib.request

import pytest

import server

OK = 200


@pytest.fixture()
def server_url():
    """Start the server on a free port for the test, then stop it."""
    httpd, port = server.make_server(port=0)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{port}"
    httpd.shutdown()


def test_health_returns_ok(server_url):
    """The health endpoint reports the server is up."""
    with urllib.request.urlopen(f"{server_url}/api/health") as response:
        assert response.status == OK
        body = json.load(response)
    assert body == {"status": "ok"}
