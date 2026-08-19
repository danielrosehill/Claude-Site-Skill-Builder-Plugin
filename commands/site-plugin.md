---
description: Build or extend a Claude Code plugin for a website by observing it in the browser — intake, observe, propose, approve, author.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, Agent
---

Build a site plugin for the target the user names, driving their own browser.

Run the pipeline, stopping where each skill says to stop:

1. `site-recon-intake` — target, page list or exploratory brief, account posture,
   constraints, target repo, private workspace.
2. `pick-browser-route` — prove the route on one page before building on it.
3. `observe-page` — walk the page list; one observation note per surface.
4. `map-site-api` — only where a JSON endpoint would be a more durable handle than
   the markup.
5. `propose-site-skills` — present the roster and **wait for per-line approval**.
6. `write-site-profile` — the volatile facts, in one JSON file.
7. `author-durable-skill` — one per approved line; audit each with
   `skill-durability-auditor`.
8. `publication-gate` — classify the whole diff before the first commit.

If the target plugin repo does not exist, hand off to
`create-claude-plugins:new-claude-plugin` to scaffold and register it, then return.

Do not skip step 5. Do not author anything the user has not approved.
