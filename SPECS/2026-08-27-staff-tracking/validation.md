# Staff Tracking — Validation

Date: 2026-08-27
Branch: `feature/staff-tracking`

This describes how we prove the feature is complete and correct before merge.
It runs the full Red/Green cycle: tests are written first and made to pass.

## Automated checks (must all pass)

Run from the project root:

```bash
pytest                # all tests pass
mypy .                # strict type checking, no errors
ruff check .          # lint, no errors
ruff format --check . # formatting, no differences
```

## Backend API tests (part of pytest)

The pytest suite must cover:

- `GET /api/orders` returns all stored orders, most recent first.
- `POST /api/orders/<id>/status` with a valid status returns 200 and the new
  status.
- `POST /api/orders/<id>/status` with an unknown id returns 404 and the order
  list is unchanged.
- `POST /api/orders/<id>/status` with a non-numeric id returns 404.
- `POST /api/orders/<id>/status` with an invalid status value returns 400 and
  the order's status is unchanged.
- `POST /api/orders/<id>/status` with a missing `status` field returns 400.
- Existing behaviour is unchanged: `GET /api/health`, `GET /api/menu`,
  `POST /api/orders` and the customer page still work.
- A `GET /api/orders` request is logged (logging decorator).

## Manual / browser validation

1. Start the server: `python3 server.py`.
2. Place an order through the customer page (`/`).
3. Open `/staff` — the order appears with status `received`.
4. Click to advance the order — its status changes (`preparing`, then `done`),
   and the board reflects it.
5. Open `/staff` with no orders placed (after a restart) — it shows a "no
   orders yet" message instead of erroring.
6. The customer page (`/`) still works as before.

## Public URL confirmation

- `curl` the public Codio URL for `/staff` (expect 200).
- `curl` `GET /api/orders` (expect the orders JSON).
- `curl` `POST /api/orders/<id>/status` with a valid body (expect 200) and an
  invalid body (expect 400), proving the frontend/backend talk over the
  internet.

## Spec drift check (before merge)

Compare what was actually implemented against:
- SPECS/MISSION.md, SPECS/TECH.md, SPECS/ROADMAP.md
- SPECS/2026-08-27-staff-tracking/requirements.md, plan.md

If anything differs (an added field, a changed response shape, a scope
change), **surface that difference to the user and update the relevant spec
with the user's approval** before merging.

## Merge criteria

The feature may be merged to `master` only when:
- All automated checks above pass.
- The manual browser validation passes.
- Any spec drift has been confirmed with the user and the specs updated.
- A pull request has been reviewed.
