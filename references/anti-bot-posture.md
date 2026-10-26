# Bot defences: working with them, not against them

The work here is legitimate: the user automating their own account, inside a session
they signed into themselves. Bot defences don't know that. A site's WAF, bot manager
or fraud scoring sees request patterns, not intent, and an agent can trip it while
doing nothing wrong. The answer is to look like what the agent actually is, a person's
own browser being used at a person's pace. Disguising the agent as something else is never the answer.

This page is the operating posture. `publication-policy.md` sets the hard lines
(no bypasses, one attempt at a blocked route, defence observations stay private), and
this page doesn't relax any of them.

## Why the default route rarely trips anything

The user's own signed-in browser (a persistent agent browser or `claude-in-chrome`)
carries the user's real cookies, device history, IP, locale and passed-MFA state. To
the site, that is the user. Most trouble starts when a build moves off that route:
headless sweeps, fresh profiles, server IPs, plain fetches against session pages.

## Posture while observing and while skills run

- **Stay on the real session for anything signed-in.** Don't move session-bound work
  to headless or to `curl` with copied cookies. Copying session cookies out of the browser
  is out of bounds anyway.
- **Human pace.** One tab, sequential loads, a pause of a few seconds between page loads and a
  pause after each interaction. No parallel fan-out, no tight loops, no retry storms.
- **Fewer requests beats faster requests.** One captured JSON call often replaces
  twenty page loads (`network-discovery.md`). Cache within a run, and don't reload a
  page to re-read something already captured.
- **Use the UI's own cadence for its API.** When a skill calls a site endpoint
  directly, call it the way the page does: same method, same parameters, at similar
  frequency, from the page context so the session and headers come along naturally.
- **Budget the volume.** Record a sensible ceiling in the profile
  (`conduct.pace`: e.g. `"max_pages_per_run": 30, "min_seconds_between_loads": 3`)
  and make skills honour it. A skill that needs more than the ceiling should batch
  across runs or ask the user first.
- **Respect signals.** `429`, `Retry-After`, "unusual activity" banners and sudden
  extra MFA prompts all mean slow down or stop. They are not obstacles to engineer around.

## When a challenge appears anyway

A CAPTCHA, an "are you human" interstitial, a press-and-hold, a sudden re-login:

1. **Stop the run.** Don't retry, reload repeatedly, or try another route to get
   past it.
2. **Hand it to the user.** They clear it themselves in the browser they are
   watching (the remote viewer for an agent browser, or their own Chrome). The agent
   never solves, clicks through, or delegates a challenge to a solving service.
3. **Resume once**, at a slower pace. If it comes back in the same session, end the
   run and report that the surface isn't automatable at this volume. Record in the
   profile which surfaces need the user present. Leave out why.
4. **Record privately.** Anything about what the challenge looked like or what seemed
   to trigger it goes to the private workspace only.

## Out of bounds

None of these are tuning options. They are the line between using a site and evading
it, and the plugin doesn't do them in code, prose, or notes:

- spoofing or randomising user agents, fingerprints, or TLS signatures;
- stealth or "undetected" browser patches, and automation-flag hiding;
- rotating IPs or proxies to spread load or dodge limits;
- CAPTCHA-solving services or automated challenge solving;
- replaying or forging anti-bot tokens, sensor payloads, or signed headers.

If a surface is only reachable by doing one of these, it isn't a skill. Put it in
the roster's "not proposed, and why" list as *not automatable on the user's session*.
