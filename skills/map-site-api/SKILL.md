---
name: map-site-api
description: Map the JSON endpoints a site's own pages call, so skills can read data from a stable endpoint instead of scraping rendered markup.
---

# Map the site's API surface

A site's own XHR endpoints sit at rung 2 of the handle ladder: they change on a
release cadence rather than a design cadence, so a skill built on one survives
redesigns that break every selector on the page.

## Relationship to `browser-data-capture`

That plugin owns capture and inference — `observe-tab` for a live tab, `analyze-har`
for a DevTools export, `capture-via-proxy` for anything else, `generate-openapi` for a
draft spec, `create-domain-map` for the accumulated per-host map. **Use it for the
capture whenever it is installed** and treat its `endpoints.json` as the input here.

This skill is the plugin-authoring half: deciding which of those endpoints a skill
should depend on, and recording them in the profile in a form that ages well.

It runs for every observed page and isn't held back for pages where the markup looks hard.
How to capture on each browser route, and what to look for:
`references/network-discovery.md`.

## Steps

1. **Capture while driving the page normally** — the interactions the future skill
   will need, at human speed. No enumeration, no parameter fuzzing, no requests the
   UI would not have made.
2. **Filter to the site's own data endpoints.** Discard analytics, ads, consent,
   session pings, and third-party beacons.
3. **For each endpoint worth keeping**, record: method, path template with named
   placeholders, which parameters are load-bearing versus decorative, the response
   shape (field names and types, not sample values), pagination style, and how errors
   present.
4. **Record the auth mechanism by kind only** — session cookie, bearer token, none.
   Never the value. If it is unauthenticated but returns account-scoped data, stop and
   apply the incidental-finding rule in `references/publication-policy.md`.
5. **Pick a canary field** per endpoint — one field whose absence means the shape has
   changed. The drift probe checks for it.
5a. **Flag the session-check endpoint** (`/me`, `/session`, `/heartbeat`) as the
   profile's `session.probe`. It is the live-session check and the keep-alive target.
6. **Sort into publishable and private.** Endpoints the public UI calls are ordinary
   integration detail. Endpoints found only in a JS bundle and never called are not
   published, and are not built on.
7. Write the survivors into the profile's `urls` and `extraction` blocks with the
   verification date.

## Notes

Prefer a documented public API where the vendor ships one, even if it is slower or
needs a key. An internal endpoint can change without notice; that is the trade being
made, so say so in the skill's provenance line.
