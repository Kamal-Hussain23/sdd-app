# Staff Tracking — Requirements

Date: 2026-08-27
Branch: `feature/staff-tracking`
Based on: SPECS/ROADMAP.md step 3 (Staff tracking)

## Context

Customer ordering is done: customers see a menu, add items, and place an
order that the server keeps in memory with an id and status `received`. The
next step is for staff to see incoming orders and track how each one is being
processed.

This is a learning project for students. Everything stays simple, uses vanilla
HTML/CSS/JS and plain Python, and keeps all data **in memory** (no database,
no saving to disk).

## Scope (what this feature does)

- A separate staff page (`/staff`) shows every placed order.
- Each order shows its id, its items, and its current status.
- Staff advance each order through the statuses: `received` → `preparing` →
  `done`.
- The board updates to show the new status.

## Non-goals (out of scope for this feature)

- QR codes (later roadmap step).
- Payments, logins, or accounts (never in scope).
- Persisting orders to disk (never in scope — in-memory only).
- Live/automatic refresh or push notifications (a manual refresh is fine).

## Decisions (confirmed with the user)

1. **Staff page:** a separate `/staff` page served by the same server. No login
   (per the constitution).
2. **Board content:** every order with its id, items, and current status,
   showing the most recent order first.
3. **Statuses:** `received`, `preparing`, `done`. An order is created as
   `received` (by customer ordering) and staff move it on through `preparing`
   to `done`.
4. **Update mechanism:** staff call
   `POST /api/orders/<id>/status` and the board shows the new status.
5. **Backward compatibility:** the existing customer page (`/`), its
   endpoints (`/api/health`, `/api/menu`, `POST /api/orders`) are kept exactly
   as they are. Only the staff page and its endpoints are added.

## User scenarios

### 1. Staff see all orders
1. A customer places two orders (ids 1 and 2).
2. Staff open `/staff`.
3. The board shows both orders (most recent first), each with its items and
   status `received`.

### 2. Staff advance an order's status
1. Staff click "Next status" on an order (or otherwise set its status).
2. The order's status changes from `received` to `preparing`.
3. Clicking again changes `preparing` to `done`.
4. The board shows the updated status.

### 3. Invalid status is rejected
1. Staff (or a script) send a status that is not one of the allowed statuses,
   e.g. `{"status": "flying"}`.
2. The server returns 400 with a clear `{"error": "..."}` message.
3. The order's status is unchanged.

### 4. Unknown order id is rejected
1. Staff update an order id that does not exist, e.g. `/api/orders/999/status`.
2. The server returns 404 with `{"error": "order not found"}`.

## Endpoints (contract)

### `GET /api/orders`
Returns all stored orders, most recent first. Used by the staff board.
```json
{
  "orders": [
    {"order_id": 2, "items": ["Latte"], "status": "received"},
    {"order_id": 1, "items": ["Tea", "Croissant"], "status": "preparing"}
  ]
}
```

### `POST /api/orders/<id>/status`
Sets the status of the order with the given id.
- Body: `{"status": "preparing"}`
- Success: `{"order_id": <id>, "status": "preparing"}` (200)
- Unknown status value → 400 `{"error": "unknown status: <value>"}`
- Unknown order id → 404 `{"error": "order not found"}`
- Malformed body / missing `status` → 400 `{"error": "invalid status update"}`
- `<id>` not a number → 404 `{"error": "order not found"}`

### `GET /staff`
Serves the staff HTML page.

## Edge cases

- Empty orders list → the board shows a friendly "no orders yet" message.
- Order id not an integer in the URL → treated as unknown (404).
- Duplicate transitions (e.g. `done` → `preparing`) — allowed: staff may set
  any of the three allowed statuses on any order; this keeps the rule simple.
- After the server restarts, orders are gone (in-memory only); the board shows
  "no orders yet".

## Data model (in memory, shared with customer ordering)

A Python list of `Order` models: `order_id: int`, `items: list[str]`,
`status: str`. Allowed statuses are one of
`("received", "preparing", "done")`.
