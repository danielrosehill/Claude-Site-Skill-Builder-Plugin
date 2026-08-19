# Choosing a route into the site

Default to **the user's own browser**. Everything else is a fallback, and each rung
down trades away authentication, JavaScript, or fidelity.

| # | Route | Session | Renders JS | Use when |
|---|---|---|---|---|
| 1 | `claude-in-chrome` against the user's running Chrome | **The user's real logged-in session** | Yes | Default. Anything behind a login, a cart, an account page, a member price, a personalised view |
| 2 | Headless Playwright / Puppeteer | Anonymous (or a profile the user provisions) | Yes | Public pages only, when a batch of pages must be walked unattended |
| 3 | Plain HTTP fetch (`curl`, `WebFetch`, server-side fetchers) | Anonymous | No | Server-rendered pages, JSON endpoints, `robots.txt`, sitemaps — cheapest, use it wherever it actually works |

## Why the user's own browser is the default

The whole point of a site skill is usually to act **on the user's behalf inside their
own account**. Their Chrome already holds the session, the MFA state, the locale, the
saved addresses and the account-specific pricing. Reusing it means:

- no credentials are handled, stored, or typed by the agent;
- no separate login that trips a new-device check;
- what the agent sees is exactly what the user sees, so observations transfer.

It also bounds the work honestly: the agent can only reach what the user is already
entitled to reach.

The cost is that it is attended and visible — it drives a window the user is looking
at. Do not use it for long unattended sweeps; that is what rung 2 is for.

## When to drop to Playwright / Puppeteer

Only for pages that need **no session**. If a page renders differently when signed
in, rung 2 will quietly capture the signed-out variant and every skill built on it
will be wrong for the user. Check one known page under both routes before trusting a
batch capture.

Provision it as its own browser profile. Never point a headless driver at the user's
real Chrome profile directory — it corrupts the running profile's lock state.

## When plain fetch is enough

More sites than you would expect are server-rendered, and a fetch is an order of
magnitude cheaper and faster than a browser. Test it first on one representative
page: if the data is in the HTML, use fetch and note it in the profile.

Watch for the three false successes documented in `durability-doctrine.md` — a 200
can be a challenge page, a login wall, or an unhydrated shell.

## Interact semantically, never by coordinate

Driving a real browser makes coordinate clicking the easy path, and it is the single
most brittle thing a site skill can contain — it breaks on a window resize, a zoom
level, a scroll position, or a cookie banner, with the page itself unchanged.

Read the page, locate the element by role, accessible name, label or visible text, and
act on the reference the read returns. Screenshots are evidence for a human, not a
handle for a skill. See `durability-doctrine.md`.

## Blocked routes

A blocked route is a signal about intent, not a puzzle. Record which routes work and
which do not, choose one that works, and move on. Do not iterate against a
challenge, and do not record how the challenge decides — see `publication-policy.md`.

## Recording the decision

The chosen route belongs in the site profile, with the date and how it was checked:

```json
"access": {
  "default_route": "claude-in-chrome",
  "fallback_route": "fetch",
  "requires_session": true,
  "verified": "2026-08-20",
  "verified_how": "one product page and one account page under both routes"
}
```
