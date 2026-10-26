---
description: Re-verify a site plugin against the live site and repair what the site has changed underneath it.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, Agent
---

Check a site plugin for drift and repair it.

1. `drift-probe` — routes, identity, handles, endpoint canaries, in one sequential
   pass. Report `OK` / `CHANGED` / `BLOCKED` per check and name the affected skills.
2. `repair-broken-skill` — for each failure: reproduce once, re-observe, fix in the
   profile where possible, and climb the handle ladder while you are in there.
3. `publication-gate` — before committing the repair.
4. `close-out-session` — stop keep-alives, close the agent's tabs, report.

Update `verified` dates only for what was actually re-checked. Report anything that
broke for the third time as a signal that the surface is not stable enough to build
on.
