---
name: pick-browser-route
description: Decide how to reach a site — the user's own signed-in Chrome by default, headless Playwright for public pages, plain fetch when it works.
---

# Pick a browser route

Choose the cheapest route that returns what the user actually sees, then prove it on
one page before a batch of observations is built on it.

Full ladder and rationale: `references/browser-routes.md`.

## Steps

1. **Test plain fetch first** on one representative page. If the data is in the HTML,
   fetch is the route for that surface — an order of magnitude cheaper than a browser.
   Classify the body before believing it: a 200 can be a challenge, a login wall, or
   an unhydrated SPA shell.
2. **If the page needs a session, or renders client-side, use `claude-in-chrome`**
   against the user's running Chrome. This is the default for anything behind a login.
   Load the browser tools in one `ToolSearch` call, take a tab context first, and open
   a new tab rather than borrowing one the user is working in.
3. **Confirm the session is live** — load an account-only page and check for the
   user's own identity on it, not just a 200. A signed-out redirect that renders a
   marketing page is the classic false positive.
4. **Drop to headless Playwright or Puppeteer only for public pages** that must be
   walked unattended. Verify one page against route 1 or 2 first: if it differs when
   signed in, headless is capturing the wrong variant. Use a dedicated profile, never
   the user's live Chrome profile directory.
5. **If a route is blocked**, note it once and route around. One attempt, then stop —
   see the conduct section of `references/publication-policy.md`.
6. Record the decision in the profile's `access` block with the date and how it was
   checked.

## Notes

Different surfaces of one site often want different routes — an open catalogue by
fetch, a signed-in cart by browser. Record per surface, not per site.
