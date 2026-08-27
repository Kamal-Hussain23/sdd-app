# Cafe Ordering System

A learning project: a working cafe ordering system built with plain web
technology.

- **Customers** scan a QR code at their table to open the menu and place an
  order.
- **Staff** see incoming orders and track how each one is being processed.

## How it's built

- **Backend:** a small Python web server. Orders and the menu live **in
  memory** — there is no database and nothing is saved to disk.
- **Frontend:** plain HTML, CSS, and vanilla JavaScript (no React, no
  libraries).

## Set up and run

The backend is a plain Python server with no extra libraries to install.

Run it from the project root:

```bash
python3 server.py
```

Then open the site at:

- `http://localhost:3000/` (on this machine)
- or the public Codio URL: `https://${CODIO_HOSTNAME}-3000.codio.io/`

Click the **Check server** button to confirm the frontend can reach the
backend's health endpoint.

(For now the app is just a walking skeleton: a health check plus the page that
talks to it. Ordering comes next.)

## Where to find the constitution

- **SPECS/MISSION.md** — the project's purpose, values, and out-of-scope items
- **SPECS/TECH.md** — what we build with and how we write code
- **SPECS/ROADMAP.md** — current state, next steps, and long-term vision

Details of individual features live in dated folders under `SPECS/`, not in the
constitution.
