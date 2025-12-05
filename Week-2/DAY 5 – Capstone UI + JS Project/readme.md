# Mini E-commerce — Summary

## Project overview
A small front-end mini e‑commerce UI that fetches products from https://dummyjson.com, displays them in cards, and supports search, sort, and category filtering.

## Files
- `index.html` — page structure, header, controls, product container.
- `style.css` — responsive styles, grid layout, card styles, header and controls.
- `script.js` — fetches products and provides UI behavior (search, sort, category filter, render).

## What I learned
- Fetching remote data using `fetch` with `async/await`.
- Working with JSON responses and keeping state in a module-level array (`products`).
- Rendering UI by manipulating `innerHTML` and using template literals.
- Filtering and sorting arrays with `.filter()` and `.sort()`.
- Attaching DOM event listeners (`input`, `change`, `click`) and updating the UI in response.
- Simple responsive layout using CSS Grid and media queries.
- Basic UI patterns: search-as-you-type, sort dropdown, category tabs, and card components.

## Key implementation notes
- Data load:
  - `loadProducts()` fetches data and calls `displayProducts(products)`.
- Search:
  - Filters `products` by title (case-insensitive) on `input`.
- Sort:
  - Uses a shallow copy (`[...products]`) and sorts by `price` on `change`.
- Category filter:
  - Category buttons toggle `active` class and filter the displayed list by `category`.
