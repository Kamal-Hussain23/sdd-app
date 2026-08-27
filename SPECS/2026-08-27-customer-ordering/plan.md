# Customer Ordering — Plan

Date: 2026-08-27
Branch: `feature/customer-ordering`

This is a Red/Green TDD repo. For every task group below, **write the failing
test first (red), then implement to make it pass (green), then refactor**.
Run the checks listed at each step.

## Task group 1 — Data models (contracts)

Create simple, typed models for the menu and orders. Keep business logic
separate and use clear types (per SPECS/TECH.md).

- Define an `Item` model: `name: str`, `price: float`.
- Define an `Order` model: `order_id: int`, `items: list[str]`,
  `status: str`.
- Define the in-memory `menu: list[Item]` and a place to hold
  `orders: list[Order]` with a counter for the next order id.

**Checks:** `pytest` (red → green), `mypy`, `ruff lint`, `ruff format`.
A small unit test can assert the models construct with their fields.

## Task group 2 — Place an order (backend logic, no HTTP yet)

Implement pure order logic that can be unit-tested without a server, then wrap
it in HTTP in the next group:

- A function `place_order(items: list[str]) -> Order` that:
  - validates every item name exists in the menu (exact match against the
    menu contract — **no regexes**),
  - assigns the next `order_id`,
  - appends the `Order` to the in-memory list,
  - sets `status` to `"received"`.
- Raise a clear error (e.g. a custom `UnknownItemError`) when an item is not on
  the menu, and handle the empty/invalid cases with a general `InvalidOrderError`.

**Tests (red first):** placing a valid order returns `order_id`, `status`, and
stores it; an unknown item raises; empty items raises.

**Checks:** `pytest`, `mypy`, `ruff`.

## Task group 3 — Logging decorator

Add comprehensive logging kept separate from the business logic, using a
**decorator** (per the feature requirements). Log the request method and path,
and the outcome (success or error) of each handled request.

- Create a decorator that wraps a handler method, records a message when it
  runs (and on error), and keeps the business method itself free of logging.
- Replace the current quiet `log_message` so logs still appear, but keep tests
  quiet (or capture logs in tests).

**Tests:** verify the decorator calls the wrapped function and logs on success
and on error.

**Checks:** `pytest`, `mypy`, `ruff`.

## Task group 4 — HTTP endpoints for menu and orders

Wire the logic to the server handler:

- `GET /api/menu` → `{"menu": [...]}` from the in-memory menu.
- `POST /api/orders` → parse the JSON body, require `{"items": [...]}`, call
  `place_order`, and return `{"order_id": ..., "status": "received"}` with a
  201 status. On `UnknownItemError` or `InvalidOrderError`, return 400 with
  `{"error": "..."}`.
- Keep `GET /api/health` and the existing page.

**Tests (red first):** using the existing `server_url` fixture pattern —
GET /api/menu returns the menu; POST a valid order returns 201 and the order
id; POST an unknown item returns 400; POST empty/malformed returns 400;
`/api/health` still returns `{"status": "ok"}`.

**Checks:** `pytest`, `mypy`, `ruff lint`, `ruff format`.

## Task group 5 — Frontend menu + order page

Extend `frontend/index.html` (keep the existing "Check server" button):

- On load, `fetch("/api/menu")` and render each item with its name and price
  and an "Add" button.
- Tapping "Add" puts the item into a client-side cart (a JS array).
- Show the cart (a running list of chosen items).
- A "Place order" button `fetch("/api/orders", ...)` with the JSON body
  `{"items": [...]}`; show the returned order id or an error message.

This part is vanilla JS only — no libraries or frameworks.

**Checks:** manual browser test (see validation.md); `npm run lint` /
`npm test` only if scripts are added — otherwise reproduce by eye and via
API tests.

## Task group 6 — Documentation and final checks

- Update README.md "Set up and run" so the ordering flow is described.
- Update SPECS/ROADMAP.md step 2 to mark customer ordering done when validated.
- Run the full check suite: `pytest`, `mypy .`, `ruff check .`,
  `ruff format --check .`.
- Serve the site and confirm the public Codio URL responds.
