---
name: site-recon-intake
description: Start building a plugin for a website — capture the target, the page list, the account posture, and what the skills must do. Run this first.
---

# Site recon intake

Opens a site-plugin build. Everything downstream reads the brief this produces, so it
is worth five minutes of questions rather than five hours of the wrong observations.

## Inputs to gather

1. **Target** — the site, and the market if it varies by country (`uline-us`,
   `zap-il`). One profile per market.
2. **The user's relationship to it** — do they have an account, and is the work meant
   to happen inside it? Skills that act on the user's own account are the normal case
   and set the default route to their own browser.
3. **The brief.** Two shapes, and the user will say which:
   - **Directed** — "here are the pages, and here is what I want to be able to ask."
     Take the page list verbatim; do not add pages without saying so.
   - **Exploratory** — "look at the site signed in and propose skills." Then the
     approval gate in `propose-site-skills` is mandatory before anything is written.
4. **Target repo** — the plugin repo being built. If it does not exist, hand off to
   `create-claude-plugins:new-claude-plugin` to scaffold and register it, then return.
5. **Private workspace** — where captures go. `browser-data-capture:init-private-repo`
   provisions one if there isn't one; see `references/repo-layout.md`.
6. **Constraints** — anything the plugin must never do on this site (order, pay,
   message a seller, change settings). Record these verbatim; they become the
   profile's `conduct.never[]`.

## Steps

1. Read `references/publication-policy.md` before observing anything. The
   classification rules apply from the first note, not at commit time.
2. Fetch and read `https://<host>/robots.txt` and skim the terms of service for
   automation and account-sharing clauses. Record what they say — including when they
   say nothing — in `notes/ground-rules.md` in the target repo.
3. Confirm the user is authorised for what they are asking: their own account, or a
   public surface. If a request needs someone else's data, say so and stop.
4. Write `notes/brief.md` in the target repo: target, market, page list, the
   questions the skills must answer, constraints, date.
5. Run `pick-browser-route` and record the outcome in the brief.

## Output

`notes/brief.md` and `notes/ground-rules.md` in the target plugin repo. No skills are
written at this stage.
