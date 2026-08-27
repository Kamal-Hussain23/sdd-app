# Roadmap

## Current state

The project is a blank slate. The tooling is set up (tests, style checks,
type checking for Python, and a `frontend/` folder), but there is no app code
yet.

## Next steps (in order)

1. **Walking skeleton.** Get the thinnest working slice end-to-end: a customer
   opens the menu page and places one order that appears somewhere. This proves
   the whole setup works.
2. **Customer ordering.** Build out the menu and ordering page — add items to
   an order and submit it.
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
