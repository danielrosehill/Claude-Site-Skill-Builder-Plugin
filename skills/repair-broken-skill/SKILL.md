---
name: repair-broken-skill
description: Fix a site skill that broke when the site changed — re-observe the surface, move the handle up the ladder, and record what moved.
---

# Repair a broken site skill

Breakage is designed into this model: skills track someone else's UI. The repair loop
is short when the provenance and the profile were written properly.

## Inputs

A `CHANGED`/`BLOCKED` line from `drift-probe`, or a user report that a skill returned
something wrong. Treat "wrong value" as more urgent than "no value" — silent
wrongness is the failure this whole approach is built to avoid.

## Steps

1. **Reproduce once** on the recorded route. Confirm the failure is drift and not a
   transient — a single retry, not a loop.
2. **Re-observe the surface** with `observe-page`. Do not patch a selector from
   guesswork; look at what the page is now.
3. **Ask why it broke**, because the answer decides the fix:
   - the handle was too specific (a class, an index) → move up the handle ladder;
   - the page moved → update `urls` in the profile;
   - the data moved to a different surface or endpoint → the skill's premise changed;
     re-scope it and tell the user;
   - the route is now blocked → change route, and do not attempt to defeat the block;
   - the data is simply gone → retire the skill rather than approximate it.
4. **Fix in the profile where possible.** If the repair is a selector, a URL template
   or an endpoint path, it belongs in the profile and no SKILL.md needs to change.
   Editing prose to fix a value is a sign the fact was in the wrong place.
5. **Strengthen the handle** on the way through — a repair is the natural moment to
   climb from rung 6 to rung 3.
6. **Re-run the skill and the probe.** Update the profile's `verified` date for what
   was actually re-checked.
7. **Record the repair** in `notes/drift-<YYYY-MM-DD>.md`: what broke, what it was
   before, what it is now, and which rung it now sits on. The pattern of what breaks
   on a given site is the thing that makes the next repair fast.
8. Run the `publication-gate` before committing.

## Notes

Three repairs on the same handle means the surface is not stable enough to build on.
Say so and propose either a different data source or retiring the skill — sustained
churn is a signal, not a chore.
