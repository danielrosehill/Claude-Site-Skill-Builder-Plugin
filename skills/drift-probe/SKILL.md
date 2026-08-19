---
name: drift-probe
description: Re-verify a site plugin's load-bearing routes and handles, and report CHANGED with what moved — before a user hits it as a wrong answer.
---

# Drift probe

Site skills decay. The probe is what turns decay into a maintenance task instead of a
confidently wrong answer.

## What it checks

For the target plugin's profile, in one sequential pass:

1. **Routes** — each entry in `access.working_routes` still returns a real page, by
   body classification rather than status code.
2. **Identity** — a known URL still resolves to the known item: canonical, title,
   echoed identifier.
3. **Handles** — for each `extraction` entry, the durable description still finds the
   value, and the value matches the recorded fixture.
4. **Endpoint canaries** — each mapped endpoint still returns its canary field.
5. **Dead routes** — anything recorded as blocked is checked once, no retries. If it
   now works, that is news too.

## Steps

1. Read `profiles/<site-id>.json` for the routes, handles and fixtures.
2. Run the checks in order, sequentially, at human speed. Stop after the first failure
   in a chain — a dead route makes downstream handle checks meaningless noise.
3. **Report per check:** `OK`, `CHANGED: <what was expected> not found at <where>`, or
   `BLOCKED: <route> refused`. Exit non-zero if anything is not `OK`.
4. **Name the affected skills** — which SKILL.md files depend on each failed check, so
   the repair has a scope.
5. Write `notes/drift-<YYYY-MM-DD>.md` with the results, and update the profile's
   `verified` date **only for the checks that passed**.
6. Hand failures to `repair-broken-skill`.

## Generating the probe

`templates/probe.py` is the starting shape: it reads the profile, runs the checks,
prints one line per check, exits non-zero on any failure. Adapt it per site rather
than generalising it — a probe that needs the browser route cannot be a plain script,
and should be a documented sequence the agent runs instead.

## Notes

Run the probe before trusting any site plugin that has not been used in weeks, and
after any report that a skill "returned something odd". Odd output is almost always
drift, and drift found by a probe costs minutes.
