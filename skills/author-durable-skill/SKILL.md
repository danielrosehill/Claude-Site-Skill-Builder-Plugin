---
name: author-durable-skill
description: Write an approved site skill so it survives small UI changes and fails loudly when it does not — handles, assertions, provenance.
---

# Author a durable site skill

Writes one approved skill into the target plugin. Read
`references/durability-doctrine.md` first — this skill is its application.

## Inputs

An approved line from `notes/skill-roster.md`, the observation note it came from, and
the profile.

## Steps

1. **Name it for the question it answers**, in the site's own vocabulary. Frontmatter
   `description` ≤140 characters, trigger-rich: the nouns and verbs the user will
   actually say.
2. **State the route and the session assumption** in the body: which browser route,
   whether a signed-in session is required, what the skill does when it is not there.
3. **Write the identity assertion first.** Before extracting anything, confirm the
   page is the one asked for — canonical URL, title, echoed identifier — and classify
   the body (real page, challenge, login wall, empty shell). Never infer success from
   a status code.
4. **Reach the data by the highest rung available**, and write the instruction as a
   description a person could follow. Put selectors in the profile as dated hints,
   never inline as the definition of the target.
5. **Never write a coordinate.** Interactions are expressed as "find the element
   whose accessible name is X, then act on it" — resolved at run time. A pixel
   position, an offset from a screenshot, or an index into a list that can reorder is
   a defect, not a shortcut.
6. **Give it a fallback ladder** — one durable handle, then the next, and an explicit
   give-up. Two ways in beats one clever selector.
7. **Define the breakage signature.** What the skill says when the site has moved:
   `CHANGED: <what> not found at <where>`. It must never return a partial result as if
   it were complete, and any script must exit non-zero.
7a. **Pace and session.** Honour the profile's `conduct.pace`
   (`references/anti-bot-posture.md`): sequential loads, and stop and hand to the user on a
   challenge. If the profile has `session.keepalive: true`, copy
   `templates/keepalive_cdp.py` into the target plugin's `scripts/` and add
   arm-at-start / stop-at-end steps from `session-keepalive`. Every skill checks the
   session first and asks the user to sign in when it has lapsed.
7b. **End with cleanup.** The skill's last step closes the tabs it opened and stops
   any keep-alive it armed (`close-out-session` steps 1–2), on success and on failure.
8. **State the limits.** What the skill does not cover, what is not on the page,
   whether the values are account-specific.
9. **Add the provenance block:**

   ```markdown
   ## Provenance

   Observed on <YYYY-MM-DD> from <note>. Handles: rung <n>. Fragile: <any rung 6–7>.
   Re-verify with `drift-probe`.
   ```

10. **Run it once against the live site** and confirm it returns what the observation
   note says it should. An unrun skill is a draft.
11. **Send the draft to the `skill-durability-auditor` agent** and fix what it flags
    before committing.

## Notes

Batches: author related skills together so they share one profile read and one
vocabulary, but run and audit each individually.
