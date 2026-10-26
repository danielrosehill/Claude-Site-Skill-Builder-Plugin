# Network discovery first

Once a build is on the browser route, the site's own network traffic is the first
thing to look at, ahead of the rendered page. Most modern apps are a thin UI over a JSON API
the page already calls with the user's session. A skill that reads that response:

- survives redesigns that break every selector (rung 2 of the handle ladder);
- returns typed fields instead of text scraped from a layout;
- is faster and cheaper per run, because it needs one request and does not render, scroll or read the
  accessibility tree;
- usually exposes more than the page shows: ids, raw numbers, timestamps, and paging
  cursors.

So capture runs on **every page you observe**, from the first one. It is not a
separate pass done only when the markup looks hard.

## How to capture, per route

Start capturing **before** the page loads, so the initial data calls are included.

| Route | Capture | Response bodies |
|---|---|---|
| `claude-in-chrome` | `read_network_requests` on the tab, `urlPattern` to filter (e.g. `/api/`, `graphql`), `clear: true` between steps so each interaction's calls are isolated | Not returned. Re-issue the same **GET** from the page with `javascript_tool` (`await fetch(url, {credentials: 'include'}).then(r => r.json())`) and record the shape |
| Persistent agent browser (CDP + MCP) | The MCP server's network tool (Playwright MCP: `browser_network_requests`) | Same in-page re-fetch, or the server's response tool if it has one |
| Recorded session | `browser-data-capture:analyze-har` on a DevTools HAR export | In the HAR |
| Anything else | `browser-data-capture:capture-via-proxy` (mitmproxy) | In the flow file |

`claude-in-chrome` quirks:
- Requests are cleared when the tab navigates to a **different domain**, so open the
  tab, then navigate inside it. Don't open a fresh tab for each page.
- Only tabs in the session's MCP tab group can be read. Take `tabs_context_mcp` first.

## A cheap pre-pass with no network tool

When the network tool is not available, the page itself can list what it fetched:

```js
performance.getEntriesByType('resource')
  .filter(e => ['fetch', 'xmlhttprequest'].includes(e.initiatorType))
  .map(e => e.name)
```

Embedded state (`__NEXT_DATA__`, `__NUXT__`, `window.__APOLLO_STATE__`, `dataLayer`,
`<script type="application/json">`) often holds the same payload the API would return.
Check it in the same pass.

## What to look for

1. **The data call behind each view:** the request whose response contains the
   values on screen. Search the captured URLs for the view's nouns (`orders`,
   `invoices`, `items`). GraphQL sites put this in the `operationName`.
2. **Identity and session calls** (`/me`, `/session`, `/user`, `/auth/refresh`,
   `/heartbeat`). These calls are the session probe and keep-alive endpoint for
   `session-keepalive`, and the live-session check for `pick-browser-route`.
3. **Pagination:** cursor, offset or page number, and where the next value is read
   from.
4. **Search and filter grammar:** how the UI's filters turn into query parameters.
   This usually replaces a whole click sequence with one URL.
5. **Writes:** `POST`/`PUT`/`DELETE` that the UI fires. Record that they exist, and never replay them.
   State-changing skills need explicit user approval of the specific action.

Hand what you find to `map-site-api`, which decides which endpoints a skill may
depend on and records them in the profile with a canary field.

## Limits

- Replay only **GET** requests the UI itself made, with the parameters it used. Do not fuzz,
  enumerate ids, or call endpoints found only in a JS bundle.
- Never record header or cookie **values**. Record the auth mechanism by kind (cookie,
  bearer, none) only.
- If an endpoint returns account data without auth, or another user's data, stop and
  apply the incidental-finding rule in `publication-policy.md`.
- Request signing, nonces and anti-bot tokens are private detail. If a call can't be
  reproduced without them, the skill drives the UI and does not call the endpoint directly.
