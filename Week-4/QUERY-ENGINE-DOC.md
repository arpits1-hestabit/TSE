# Query Engine

Purpose: describe the query language, parsing rules and examples used by the Product API's dynamic search/filter/sort/pagination engine.

## Supported query parameters
- search — text search applied as case-insensitive regex across configured fields (e.g., name, description).
- minPrice, maxPrice — numeric range limits for price.
- price — exact numeric match (optional).
- tags — comma-separated list; matches any provided tag (OR).
- sort — comma-separated list of sort directives in `field:dir` (dir = asc | desc). Example: `price:desc,name:asc`.
- page — 1-based page number (default 1).
- limit — items per page (default 20, enforced max e.g. 100).
- includeDeleted — `true|false` include soft-deleted records when true (default false).
- other fields — any direct equality filter supported (e.g., `category=mobiles`).

## Behavior & semantics

1. Search
   - `search=phone` builds a case-insensitive regex and ORs it across configured searchable fields:
     `{ $or: [ { name: /phone/i }, { description: /phone/i } ] }`
   - Escape user input to avoid regex DoS or unintended patterns.

2. Tag matching
   - `tags=apple,samsung` => `{ tags: { $in: ["apple", "samsung"] } }` (OR semantics).
   - To require all tags use a different param (not implemented here) like `allTags=` mapping to `$all`.

3. Numeric ranges
   - `minPrice` / `maxPrice` translate to Mongo range:
     `{ price: { $gte: minPrice, $lte: maxPrice } }` with absent bounds omitted.

4. Sorting
   - `sort=price:desc` => `{ price: -1 }`.
   - Support multiple comma-separated directives in order.

5. Pagination
   - `page` and `limit` calculate skip/limit:
     `skip = (page - 1) * limit`.
   - Return meta: `{ total, page, limit, totalPages }`.

6. Soft delete
   - Soft delete implemented with `deletedAt` (timestamp) + optional `isDeleted` flag.
   - Default behavior: exclude documents with `deletedAt` set (`{ deletedAt: { $exists: false } }` or `{ deletedAt: null }` depending on model).
   - `includeDeleted=true` removes that exclusion so deleted documents are returned.

7. Global error format (from exercise)
   - When query parsing fails return error shaped:
     `{ success: false, message, code, timestamp, path }`

## Example requests → Mongo filter + options

1) GET /products?search=phone&minPrice=100&maxPrice=500&sort=price:desc&page=2&limit=10&tags=apple,samsung
- Filter:
```js
{
  $and: [
    { $or: [ { name: /phone/i }, { description: /phone/i } ] },
    { price: { $gte: 100, $lte: 500 } },
    { tags: { $in: ["apple","samsung"] } },
    { deletedAt: { $exists: false } } // unless includeDeleted=true
  ]
}
```
- Options:
```js
{ sort: { price: -1 }, skip: 10, limit: 10 }
```

2) GET /products?includeDeleted=true&tags=accessory&sort=name:asc
- Filter:
```js
{ tags: { $in: ["accessory"] } }
// no deletedAt exclusion
```
- Options:
```js
{ sort: { name: 1 }, skip: 0, limit: 20 }
```



