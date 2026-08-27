"""Tests for the customer-ordering business logic (no HTTP)."""

import pytest

import server


def test_menu_has_expected_items() -> None:
    """The in-memory menu is defined and each item has a name and price."""
    assert len(server.MENU) > 0
    for item in server.MENU:
        assert isinstance(item.name, str) and item.name
        assert isinstance(item.price, (int, float))


def test_place_order_assigns_id_and_status() -> None:
    """Placing a valid order returns an order with id, items and status."""
    order = server.place_order(["Latte"])
    assert isinstance(order.order_id, int)
    assert order.items == ["Latte"]
    assert order.status == "received"


def test_place_order_stores_in_memory() -> None:
    """A placed order is kept in the in-memory orders list."""
    order = server.place_order(["Croissant"])
    assert order in server.ORDERS


def test_order_ids_increment() -> None:
    """Two orders get different, increasing ids."""
    first = server.place_order(["Latte"])
    second = server.place_order(["Tea"])
    assert second.order_id == first.order_id + 1


def test_place_order_unknown_item_raises() -> None:
    """An item not on the menu is rejected and nothing is stored."""
    before = len(server.ORDERS)
    with pytest.raises(server.UnknownItemError):
        server.place_order(["Not On The Menu"])
    assert len(server.ORDERS) == before


def test_place_order_empty_raises() -> None:
    """An empty or missing items list is rejected."""
    with pytest.raises(server.InvalidOrderError):
        server.place_order([])
