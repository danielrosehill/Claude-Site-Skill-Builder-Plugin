---
name: write-site-profile
description: Write or update the site profile JSON — the one file holding every volatile fact about a site, so a redesign is a one-file edit.
---

# Write the site profile

Every fact with a shelf life lives in `profiles/<site-id>.json`. Skills describe
method and read the profile for specifics, so when the site moves you edit one file
instead of grepping six markdown files for a class name.

Schema and worked examples: `references/site-profile-schema.md`.

## Steps

1. **Resolve the id** — host plus market where the market matters (`example-us`).
   One profile per market; do not merge two storefronts into one file.
2. **Fill the blocks** from the observation notes: `access`, `urls`, `identifier`,
   `extraction`, `not_on_the_page`, `conduct`.
3. **Date everything.** Top-level `verified` plus `verified_how` describing what was
   actually checked — "three product pages and one search under a signed-in session"
   is a claim someone can re-run; "verified" alone is not.
4. **Mark inferences as inferences.** Anything not directly observed gets
   `"verified": false` and a note. Never state an assumption in the same voice as a
   check.
5. **Record traps beside the field they trap**, not in a general notes section — the
   agent reading `extraction.price` needs to know about the missing currency symbol
   right there.
6. **Fill `conduct.never[]`** from the constraints in the brief, plus the standing
   ones: no ordering or payment, no changing account settings, no retrying a
   challenge, no parallel fan-out.
7. **Run the publication gate** over the finished file before committing. The profile
   ships publicly.
8. Validate: `python3 -c "import json,sys; json.load(open(sys.argv[1]))" profiles/<site-id>.json`

## Notes

When updating an existing profile, bump `verified` only for the parts actually
re-checked. A blanket date refresh on unverified content is worse than a stale date,
because it converts "old" into "wrong".
