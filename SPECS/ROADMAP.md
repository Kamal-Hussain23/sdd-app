# Roadmap

## Current state

The tooling is set up and the **walking skeleton is done**: a Python server
that serves a small page and a `/api/health` endpoint, wired together so the
page can fetch from the server. There is no ordering yet.

## Next steps (in order)

1. ~~**Walking skeleton.**~~ Done — server serves a page and a `/api/health`
   endpoint that the page can fetch.
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
