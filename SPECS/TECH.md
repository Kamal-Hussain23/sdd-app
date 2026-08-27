# Tech

## What we build with

- **Backend:** a small Python web server. It holds the menu and the orders
  **in memory** (like a Python list). There is **no database** — data is not
  saved to disk, and it disappears when the server restarts. That is fine for
  learning.
- **Frontend:** plain HTML, CSS, and vanilla JavaScript. **No React and no
  other libraries or frameworks.**

## How we write code

- **Test first (red/green TDD).** Write a failing test, watch it fail (red),
  then write just enough code to make it pass (green). Refactor when needed.
- **Typing.** Use clear types so mistakes are caught early (e.g. say an order
  is a list of items). Mypy runs on our Python code.
- **Don't repeat yourself (DRY).** If the same code is written twice, pull it
  out into one shared helper.
- **Walking skeleton first.** Start with the thinnest working slice of the app,
  then grow features on top of it. This stops the app from getting big and
  messy before it even works.
- **Keep business logic separate.** Keep the "how ordering works" code separate
  from things like logging or showing pages, so each part stays simple.
- **Simple over complex.** Prefer the solution that is easiest to read and
  understand, even if a fancier one seems more "professional."
