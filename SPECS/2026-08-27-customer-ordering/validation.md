# Customer Ordering — Validation

Date: 2026-08-27
Branch: `feature/customer-ordering`

This describes how we prove the feature is complete and correct before it is
merged. It always runs the full Red/Green cycle: tests are written first and
made to pass.

## Automated checks (must all pass)

Run from the project root:

```bash
pytest            # all tests pass
mypy .            # strict type checking, no errors
ruff check .      # lint, no errors
ruff format --check .   # formatting, no differences
```

## Backend API tests (part of pytest)

The pytest suite must cover:

- `GET /api/menu` returns the full in-memory menu as `{"menu": [...]}`.
- `POST /api/orders` with valid `{"items": ["Latte", "Croissant"]}` returns
  `201` and `{"order_id": <n>, "status": "received"}`.
- `POST /api/orders` with an unknown item returns `400` and an error, and no
  order is stored.
- `POST /api/orders` with empty items, a non-list body, or malformed JSON
  returns `400`, and no order is stored.
- `GET /api/health` still returns `{"status": "ok"}` (backward compatibility
  retained).
- Order ids increment (placing two orders gives 1 then 2), proving in-memory
  storage works.

## Manual / browser validation

1. Start the server: `python3 server.py`.
2. Open the site (local `http://localhost:3000/` or the public Codio URL).
3. The menu renders with item names and prices.
4. Click "Add" on a couple of items — they appear in the cart.
5. Click "Place order" — the page shows the received order number.
6. Reload the page: the menu still loads (orders themselves may reset, since
   data is in memory only and a reload is acceptable to lose the cart/menu
   state — the menu always comes from the server).
7. The existing "Check server" button still works (shows "Server says: ok").

## Public URL confirmation

- `curl` the public Codio URL for `/` (expect 200) and `POST /api/orders` with
  a valid body (expect 201 + order id).
- Confirm the page fetches the menu through the public URL, proving the
  frontend talks to the backend over the internet, not just localhost.

## Spec drift check (before merge)

Compare what was actually implemented against:
- SPECS/MISSION.md, SPECS/TECH.md, SPECS/ROADMAP.md
- SPECS/2026-08-27-customer-ordering/requirements.md, plan.md

If anything differs (e.g. an added field, a changed response shape, a scope
change), **surface that difference to the user and update the relevant spec
with the user's approval** before merging.

## Merge criteria

The feature may be merged to `master` only when:
- All automated checks above pass.
- The manual browser validation passes.
- Any spec drift has been confirmed with the user and the specs updated.
- A pull request has been reviewed.
