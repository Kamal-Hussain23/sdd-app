# Customer Ordering — Requirements

Date: 2026-08-27
Branch: `feature/customer-ordering`
Based on: SPECS/ROADMAP.md step 2 (Customer ordering)

## Context

The walking skeleton is done: a Python server serves a page and a
`/api/health` endpoint. The next step is for a customer to actually order.

This is a learning project for students. Everything must stay simple, use
vanilla HTML/CSS/JS on the frontend and plain Python on the backend, and keep
all data **in memory** (no database, no saving to disk).

## Scope (what this feature does)

- A customer opens the page and sees the menu.
- The customer adds items to a cart.
- The customer places the order, which the server stores in memory.
- The server returns an order id so the order can be tracked later.

## Non-goals (out of scope for this feature)

- Staff tracking view (that is the next roadmap step).
- QR codes (later roadmap step).
- Payments, logins, or accounts (never in scope).
- Persisting orders to disk (never in scope — in-memory only).

## Decisions (confirmed with the user)

1. **Menu source:** hardcoded in the Python server as a simple in-memory list.
2. **Menu item fields:** each item has a `name` (string) and a `price` (number).
3. **Customer flow:** see menu → add items to a cart → place the order.
4. **Order submission:** the frontend sends a `POST /api/orders` with a JSON
   body of the form `{"items": ["Latte", "Croissant"]}` — a list of item names.
5. **Server response:** on a valid order the server returns
   `{"order_id": 1, "status": "received"}`.
6. **Order storage:** the server keeps all placed orders in a Python list in
   memory (so the staff-tracking step can read them next).
7. **Backward compatibility:** keep the existing `/api/health` endpoint and the
   existing page with its "Check server" button. The menu is added below it;
   nothing from the walking skeleton is removed.

## User scenarios

### 1. Customer adds items and places an order
1. Customer opens the site and sees the menu.
2. Customer taps/click items to add them to the cart.
3. Customer taps "Place order".
4. The page shows "Order received. Your order number is 1."

### 2. Invalid order is rejected
1. Customer (or a script) posts an order with an item name that is not on the
   menu, e.g. `{"items": ["Unknown Thing"]}`.
2. The server returns an error status and a clear `{"error": "..."}` message.
3. No order is stored.

### 3. Health check still works
1. A request to `/api/health` still returns `{"status": "ok"}`.

## Endpoints (contract)

- `GET /api/health` → `{"status": "ok"}` (unchanged)
- `GET /api/menu` → the in-memory menu, e.g.
  `{"menu": [{"name": "Latte", "price": 3.5}, ...]}`
- `POST /api/orders` body `{"items": ["Latte", "Croissant"]}` →
  `{"order_id": 1, "status": "received"}` (201 Created)
  - Invalid item name → 400 with `{"error": "unknown item: <name>"}`
  - Malformed body (not a list, missing `items`, empty) → 400 with
    `{"error": "invalid order"}`

## Edge cases

- Empty `items` list → rejected with 400.
- `items` not a list, or body not valid JSON → rejected with 400.
- An empty menu item name, or a request with no body at all → rejected with 400.
- Duplicate item names in one order are allowed and counted (the customer
  really wants two of that item).
- An item name appearing twice in the menu itself is a setup error and is
  avoided when defining the menu; the order validation simply matches exact
  names in the menu.

## Data model (in memory)

Menu: a Python list of `Item` models, each with `name: str` and `price: float`.

Stored orders: a Python list of `Order` models, each with an auto-incremented
`order_id: int`, `items: list[str]`, and `status: str` (initially `"received"`).
