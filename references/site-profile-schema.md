# The site profile

One JSON file per site, at `profiles/<site-id>.json` in the plugin being built. It is
the single place volatile facts live, so that a site change is a one-file edit.

`<site-id>` is host plus market where the market matters: `uline-us`, `amazon-us`,
`zap-il`.

## Required top level

```json
{
  "id": "example-us",
  "name": "Example (US)",
  "host": "www.example.com",
  "currency": "USD",
  "verified": "2026-08-20",
  "verified_how": "signed-in Chrome session; three product pages and one search",
  "requires_session": true,
  "access": {},
  "urls": {},
  "identifier": {},
  "extraction": {},
  "not_on_the_page": {},
  "conduct": {}
}
```

## The blocks

**`access`** — `default_route`, `fallback_route`, `working_routes[]`, `dead_routes[]`,
`session_needed_for`. Plain statements of what reaches the site. No defence analysis.

**`urls`** — templates with named placeholders: `"detail":
"https://host/p/{id}"`. Note when a slug is cosmetic, because a wrong slug that still
resolves is how a skill silently returns the wrong product.

**`identifier`** — what the site calls its primary key, its regex, examples, and what
it does *not* mean (a model number is often not a manufacturer part number, and often
identifies a group of variants rather than one item).

**`extraction`** — per data point: the handle ladder rung used, the durable
description, the observed selector as a dated hint, and the assertion that proves the
right element was found.

```json
"extraction": {
  "price": {
    "rung": 3,
    "find": "JSON-LD Product.offers.price on the detail page",
    "fallback": "the table whose header row reads PRICE; the row whose first cell is the model number",
    "selector_hint": "table.priceChart",
    "hint_verified": "2026-08-20",
    "assert": "the row's model cell equals the requested model",
    "traps": ["only the first row prints a currency symbol"]
  }
}
```

**`not_on_the_page`** — what a caller will ask for and the page cannot answer: stock,
freight, delivery date. Prevents the next agent inventing it.

**`session`** (when `requires_session`): `idle_timeout_minutes` (observed, or
`null`), `timeout_signal`, `probe` (the site's own session-check path), `keepalive`
(true when skills must arm `session-keepalive`), `verified`. Timings and signals only.

**`conduct`** — `never[]`: the actions this plugin will not take on this site
(ordering, changing account settings, retrying a challenge, parallel fan-out).
`pace`: `max_pages_per_run`, `min_seconds_between_loads`. Skills honour it; see
`anti-bot-posture.md`.

## Rules

- Every fact carries the date it was verified, or it inherits the top-level `verified`.
- Anything unverified is labelled `"verified": false` with a note — never asserted in
  the same voice as something checked.
- Nothing from the "private" or "never" columns of `publication-policy.md` enters this
  file. It ships in the public repo.
