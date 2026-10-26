---
name: session-keepalive
description: Detect a signed-in session timing out mid-build or mid-run, and keep it alive with a bounded periodic ping only while the agent is actively driving it.
---

# Session timeout detection and keep-alive

Some apps sign the user out after a few minutes idle. A build that pauses to write
notes, or a skill run that waits on the user, comes back to a login wall. If it's
missed, every observation after that point is of the login page.

## Detect it

Treat any of these as a timeout and stop extracting:

- the tab's URL moves to a sign-in path, or the page identity check fails because the
  heading is now "Sign in";
- a captured data call returns `401`/`403`/`419`/`440`, or redirects;
- a "Your session is about to expire" or "You've been signed out" dialog;
- the user's own identity (name, avatar, account id) disappears from the page.

When it happens: **ask the user to sign in again in the browser they are
watching.** The agent never types credentials and never re-authenticates by itself.
Then re-check identity and resume from the last confirmed step.

Record what was observed in the profile's `session` block. Write down the timing and
the signal, and leave out any defence analysis:

```json
"session": {
  "idle_timeout_minutes": 15,
  "timeout_signal": "redirect to /login; /api/me returns 401",
  "probe": "/api/me",
  "keepalive": true,
  "verified": "YYYY-MM-DD"
}
```

## Fix it, in order of preference

1. **The site's own option.** "Keep me signed in", "Remember this device", or a longer
   session setting. The user turns it on themselves; it is an account setting, so the
   agent only suggests it.
2. **Accept the warning dialog** the site shows before expiry ("Stay signed in"), when
   it appears during an active run. It is a normal UI action.
3. **A bounded keep-alive ping** while the session is being driven. It requests the site's own
   session-check endpoint (found in `references/network-discovery.md` — `/me`,
   `/session`, `/heartbeat`) from inside the site's tab, at an interval comfortably
   under the timeout.

### Keep-alive on a CDP browser (persistent agent browser)

`templates/keepalive_cdp.py` is a self-contained CLI (`uv run --script`):

```bash
uv run --script scripts/keepalive_cdp.py \
  --cdp http://127.0.0.1:9222 --origin https://app.example.com \
  --ping /api/me --every 240 --max-minutes 60 --stop-file /tmp/<site-id>.stop &
```

It prints one JSON line per ping, exits `3` with an `expired` event if the session has
already gone, and stops itself at `--max-minutes`, when the stop file appears, or when
the tab closes. Run it in the background for the active stretch. `touch` the stop file
at close-out.

### Keep-alive on `claude-in-chrome`

There is no CDP endpoint, so run the ping inside the page. Open a **dedicated tab** on a
light page of the site (so navigation in the working tab doesn't kill the timer), then
inject with `javascript_tool`:

```js
const k = window.__siteKeepalive;
if (k) clearInterval(k.id);
window.__siteKeepalive = {
  started: Date.now(), maxMs: 60 * 60e3, last: null,
  id: setInterval(async () => {
    const s = window.__siteKeepalive;
    if (Date.now() - s.started > s.maxMs) { clearInterval(s.id); s.last = 'max-reached'; return; }
    try {
      const r = await fetch('/api/me', {credentials: 'include', redirect: 'manual', cache: 'no-store'});
      s.last = {t: new Date().toISOString(), status: r.status, type: r.type};
    } catch (e) { s.last = {error: String(e)}; }
  }, 240e3),
};
'keepalive armed'
```

Check `window.__siteKeepalive.last` between steps. A `401`/`403` or
`opaqueredirect` means the session is already gone. The timer dies when the tab is
closed, which close-out does.

## Bounds

- **Only while the session is being actively driven.** Arm it at the start of an active
  stretch and stop it at close-out. Never leave a ping running unattended, overnight,
  or "for next time".
- Always set a hard maximum (`--max-minutes` / `maxMs`). Default 60 minutes; re-arm
  explicitly if the work genuinely runs longer.
- Ping one read-only endpoint the site itself calls, no more often than needed (the
  timeout minus a margin; never under a minute).
- A keep-alive keeps an existing session open. It doesn't extend what the account is
  entitled to, and it never replaces signing in.

## In a built plugin

When the profile says `"keepalive": true`, `author-durable-skill` copies
`templates/keepalive_cdp.py` into the target plugin's `scripts/`, puts the in-page
snippet in the skill body, and makes arm-at-start and stop-at-end explicit steps of
every skill that runs long enough to need it.
