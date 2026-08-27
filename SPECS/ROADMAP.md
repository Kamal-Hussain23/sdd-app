# Roadmap

## Current state

The **walking skeleton**, **customer ordering**, and **staff tracking** are
done. A customer can see the menu, add items, and place an order. Staff can
open a separate page (`/staff`) to see all orders and advance each one through
`received` → `preparing` → `done`. All data is in memory and resets when the
server restarts. There is no QR code yet.

## Next steps (in order)

1. ~~**Walking skeleton.**~~ Done — server serves a page and a `/api/health`
   endpoint that the page can fetch.
2. ~~**Customer ordering.**~~ Done — see the menu, add items, place an order.
   See SPECS/2026-08-27-customer-ordering/.
3. ~~**Staff tracking.**~~ Done — a `/staff` page lists orders and let staff
   advance each through `received` → `preparing` → `done`. See
   SPECS/2026-08-27-staff-tracking/.
4. **QR code.** Generate a QR code that opens the ordering page for a table.
5. **Polish.** Nice styling and clearer messages.

## Longer-term vision

A fuller ordering flow — for example tracking order status live, or a way to
manage the menu from the staff side.

## Guiding rule

Each step starts from the smallest thing that works (the walking skeleton) and
grows from there. We avoid adding features before the basics work.
