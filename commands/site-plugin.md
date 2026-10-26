---
description: Build or extend a Claude Code plugin for a website by observing it in the browser — intake, observe, propose, approve, author.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, Agent
---

Build a site plugin for the target the user names, driving their own browser.

Run the pipeline, stopping where each skill says to stop:

1. `site-recon-intake` — target, directed URL list or exploratory brief, account
   posture, constraints, target repo, private workspace.
2. `pick-browser-route` — prove the route on one page before building on it.
3. `survey-site-surface` — **exploratory brief only**: walk the nav and network
   calls, short-list pages, and wait for the user's picks. Skip for a directed URL list.
4. `observe-page` — walk the page list with network capture on; one observation
   note per surface.
5. `map-site-api` — every page: which of the captured endpoints skills should depend on.
6. `propose-site-skills` — present the roster and **wait for per-line approval**.
7. `write-site-profile` — the volatile facts, in one JSON file.
8. `author-durable-skill` — one per approved line; audit each with
   `skill-durability-auditor`.
9. `publication-gate` — classify the whole diff before the first commit.
10. `close-out-session` — stop keep-alives, close the agent's tabs, push, report.

Throughout: pace and challenges per `references/anti-bot-posture.md`; if the session
lapses, `session-keepalive`.

If the target plugin repo does not exist, hand off to
`create-plugins:new-claude-plugin` to scaffold and register it, then return.

Do not skip step 6. Do not author anything the user has not approved. Run step 10
even when the build stops early.
