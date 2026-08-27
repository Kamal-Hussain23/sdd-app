# Staff Tracking — Plan

Date: 2026-08-27
Branch: `feature/staff-tracking`

This is a Red/Green TDD repo. For every task group below, **write the failing
test first (red), then implement to make it pass (green), then refactor**.
Run the checks listed at each step.

The existing code lives in `server.py` (models, `place_order`, handler
routing) and the tests in `tests/`. We add staff behaviour without changing
existing behaviour.

## Task group 1 — Status contract and business logic

- Define the allowed statuses as a fixed contract, e.g.
  `VALID_STATUSES = ("received", "preparing", "done")`. `received` is the
  starting status set by `place_order`.
- Add a function `get_orders() -> list[Order]` that returns the in-memory
  orders, most recent first (highest id first).
- Add a function `update_order_status(order_id: int, status: str) -> Order`:
  - raises `UnknownOrderError` if no order has that id,
  - raises `InvalidStatusError` if `status` is not in `VALID_STATUSES`,
  - sets the order's status and returns it.

Prefer explicit contracts/exceptions over stringly-typed ad-hoc checks and
avoid regexes.

**Tests (red first):** `get_orders` returns newest-first; `update_order_status`
changes an order's status; unknown id raises `UnknownOrderError`; invalid
status raises `InvalidStatusError`.

**Checks:** `pytest`, `mypy`, `ruff check`, `ruff format --check`.

## Task group 2 — HTTP endpoints

Wire the logic into `CafeHandler`:

- `GET /api/orders` → `{"orders": [...]}` using `get_orders`.
- `POST /api/orders/<id>/status`:
  - parse the `<id>` from the path (try `int()` on the id segment — a precise
    parse, not a regex);
  - read the JSON body and require a `status` field;
  - on success return `{"order_id": ..., "status": ...}` (200);
  - on `UnknownOrderError` or an unparseable id → 404 `{"error": "order not found"}`;
  - on `InvalidStatusError` → 400 `{"error": "unknown status: <value>"}`;
  - on a malformed body (missing `status`) → 400
    `{"error": "invalid status update"}`.
- `GET /staff` → serve the staff HTML page.

Keep existing routes (`/api/health`, `/api/menu`, `POST /api/orders`, `/`)
exactly as they are.

**Tests (red first):** `GET /api/orders` returns the stored orders newest
first; `POST .../status` updates a status (200); unknown id → 404; invalid
status → 400; missing status field → 400; non-numeric id → 404; existing
endpoints still work.

**Checks:** `pytest`, `mypy`, `ruff check`, `ruff format --check`.

## Task group 3 — Logging

Ensure the new request paths are covered by the existing `@log_request`
decorator (log the method and path, and errors). Add a small test that a
`GET /api/orders` request is logged.

**Checks:** `pytest`, `mypy`, `ruff`.

## Task group 4 — Staff frontend page

Add a `/staff` page (a new HTML file, e.g. `frontend/staff.html`) using vanilla
JS that:

- on load, `fetch("/api/orders")` and render each order with its id, items,
  and status;
- for each order, a button that `POST`s the next status to
  `/api/orders/<id>/status` and then re-fetches the board;
- shows a friendly "no orders yet" message when the list is empty.

Serve it from `GET /staff`. Keep the customer page (`frontend/index.html`)
unchanged.

**Checks:** manual browser test (see validation.md); the backend API is already
covered by pytest.

## Task group 5 — Documentation and final checks

- Update README.md so the staff flow is described.
- Update SPECS/ROADMAP.md to mark staff tracking done when validated.
- Run the full check suite: `pytest`, `mypy .`, `ruff check .`,
  `ruff format --check .`.
- Serve the site and confirm the public Codio URL responds for `/staff`,
  `/api/orders`, and a status update.
