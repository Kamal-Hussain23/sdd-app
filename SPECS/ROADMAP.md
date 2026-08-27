# Roadmap

## Current state

The **walking skeleton** and **customer ordering** are done. A customer can
open the page, see a menu served by the Python server, add items to a cart,
and place an order. Orders are stored in memory and given an order id. There
is no staff view or QR code yet.

## Next steps (in order)

1. ~~**Walking skeleton.**~~ Done — server serves a page and a `/api/health`
   endpoint that the page can fetch.
2. ~~**Customer ordering.**~~ Done — see the menu, add items, place an order.
   See SPECS/2026-08-27-customer-ordering/.
3. **Staff tracking.** Build the staff view to see incoming orders and mark
   each one as being processed or done.
4. **QR code.** Generate a QR code that opens the ordering page for a table.
5. **Polish.** Nice styling and clearer messages.

## Longer-term vision

A fuller ordering flow — for example tracking order status live, or a way to
manage the menu from the staff side.

## Guiding rule

Each step starts from the smallest thing that works (the walking skeleton) and
grows from there. We avoid adding features before the basics work.
