"""Tests for the staff-tracking business logic (no HTTP)."""

from collections.abc import Iterator

import pytest

import server

TwoOrders = tuple[server.Order, server.Order]


@pytest.fixture()
def clean_orders() -> Iterator[None]:
    """Empty the in-memory orders before each test."""
    server.ORDERS.clear()
    yield
    server.ORDERS.clear()


@pytest.fixture()
def two_orders(
    clean_orders: None,
) -> Iterator[TwoOrders]:
    """Create two orders and return them (first placed has the lower id)."""
    first = server.place_order(["Latte"])
    second = server.place_order(["Tea", "Croissant"])
    yield first, second


def test_valid_statuses_are_defined() -> None:
    """The three staff lifecycle statuses are part of the contract."""
    assert server.VALID_STATUSES == ("received", "preparing", "done")


def test_get_orders_returns_newest_first(two_orders: TwoOrders) -> None:
    """Most recent order (higher id) comes first."""
    lst = server.get_orders()
    assert [o.order_id for o in lst] == [two_orders[1].order_id, two_orders[0].order_id]


def test_update_order_status_changes_status(two_orders: TwoOrders) -> None:
    """Setting a valid status updates and returns the order."""
    target_id = two_orders[0].order_id
    updated = server.update_order_status(target_id, "preparing")
    assert updated.order_id == target_id
    assert updated.status == "preparing"
    assert server.ORDERS[0].status == "preparing"


def test_update_order_status_unknown_id_raises(two_orders: TwoOrders) -> None:
    """Updating an order id that does not exist raises UnknownOrderError."""
    with pytest.raises(server.UnknownOrderError):
        server.update_order_status(999, "preparing")


def test_update_order_status_invalid_status_raises(two_orders: TwoOrders) -> None:
    """A status that is not in the contract raises InvalidStatusError."""
    target_id = two_orders[0].order_id
    with pytest.raises(server.InvalidStatusError):
        server.update_order_status(target_id, "flying")
    # status is unchanged
    assert server.ORDERS[0].status == "received"
