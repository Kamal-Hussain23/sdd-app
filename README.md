# Cafe Ordering System

A learning project: a working cafe ordering system built with plain web
technology.

- **Customers** scan a QR code at their table to open the menu and place an
  order.
- **Staff** see incoming orders and track how each one is being processed.

## How it's built

- **Backend:** a small Python web server built with only the Python standard
  library. The menu and orders live **in memory** — there is no database and
  nothing is saved to disk.
- **Frontend:** plain HTML, CSS, and vanilla JavaScript (no React, no
  libraries).

## What works now

- A customer opens the page and sees the menu (served by the server).
- The customer adds items to a cart and places an order.
- The server validates the order and stores it in memory, returning an order
  number.
- Staff open a separate page (`/staff`) to see all orders and advance each one
  through `received` → `preparing` → `done`.

## Set up and run

There are no libraries to install. Run it from the project root:

```bash
python3 server.py
```

Then open the site at:

- `http://localhost:3000/` (on this machine)
- or the public Codio URL: `https://${CODIO_HOSTNAME}-3000.codio.io/`

On the **customer page** (`/`) you can:
- Click **Check server** to confirm the frontend can reach the backend.
- Add items from the menu to your cart, then click **Place order** to send the
  order. The page shows your order number.

Open the **staff page** (`/staff`) to see incoming orders and advance each
order's status.

(Orders live only in memory, so they reset when the server restarts. QR codes
come later.)

## Where to find the constitution

- **SPECS/MISSION.md** — the project's purpose, values, and out-of-scope items
- **SPECS/TECH.md** — what we build with and how we write code
- **SPECS/ROADMAP.md** — current state, next steps, and long-term vision

Details of individual features live in dated folders under `SPECS/`, not in the
constitution.
