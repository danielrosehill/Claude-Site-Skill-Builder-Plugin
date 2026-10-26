---
name: survey-site-surface
description: Exploratory brief — walk a signed-in site's navigation and network calls and propose which pages are worth wrapping in skills, before observing any in depth.
---

# Survey the site surface

For the **exploratory** brief ("look around the app and tell me what's worth
building"). It produces a short-list of candidate pages for the user to confirm.
`observe-page` then studies each one in depth.

For a **directed** brief, where the user supplied the URLs, skip this skill. Take the
list verbatim and go to `observe-page`. If one of their URLs fails to load, redirects
somewhere else, or needs a permission the account doesn't have, report it and don't
substitute a page of your own choosing.

## Inputs

`notes/brief.md` (target, account posture, constraints), the route chosen by
`pick-browser-route`, and the user's stated purpose, if any ("I mostly use it for
invoices").

## Steps

Sequential, at human pace, read-only. Follow `references/anti-bot-posture.md`
throughout.

1. **Open one tab and start network capture** before the first load
   (`references/network-discovery.md`). Keep the same tab for the whole survey so the
   capture isn't cleared.
2. **Map the navigation, not the content.** From the signed-in home page, read the
   primary nav, account menu, settings index, footer and any sitemap or
   `/sitemap.xml`. List each destination with its URL template. Don't follow
   destructive or state-changing entries ("Delete", "Cancel plan", "Pay"). Note that they
   exist and move on.
3. **Visit each top-level section once.** For each, record in a line or two:
   - what the user can learn or do there;
   - the data calls it fired (endpoint path, method, and whether the response looked like
     a list, a record, or a search);
   - whether the URL is stable and parameterised (`/orders/{id}`, `?status=open`)
     or opaque;
   - whether it is read-only or state-changing.
4. **Stop at breadth.** Go one level into a section only where a list leads to a
   detail page (a list of orders leads to one order). Don't page through results or open more
   than one sample detail per type.
5. **Score suitability** for each candidate page:

   | Factor | Good | Poor |
   |---|---|---|
   | Data access | a clean JSON call or structured data | only visual layout, canvas, or PDFs |
   | Addressability | stable URL with an id or filter params | reached only by a click sequence |
   | Action | read-only | writes, payments, messages |
   | Value | answers something the user asks repeatedly | one-off settings |
   | Session | stable sign-in | short idle timeout, frequent re-auth or challenges |

6. **Present the short-list** and stop:

   ```
   Surface of <site> (signed in, <date>):

   Worth wrapping:
   1. <page/section> — <URL template> — <what a skill would answer>
      Data: <endpoint or structured data>   Read-only: yes   Suitability: high
   2. ...

   Seen, not recommended:
   - <section> — <why: state-changing / no data / opaque URL / challenge>

   Session: <idle timeout observed or "none seen">   Endpoints found: <n>
   ```

7. **Wait** for the user to tick pages. The ticked list becomes the page list in
   `notes/brief.md`, marked as from the survey, and goes to `observe-page`.

## Output

`notes/surface-survey.md` in the target repo: the navigation map, the per-section
lines, the endpoint list (paths and shapes only), and the user's picks with the date.
Classify each line against `references/publication-policy.md` as you write it.
Account-bound values go to the private workspace.

## Notes

The survey should be cheap: a dozen or two page loads for most apps. If the
app is huge, survey the sections the user named as their purpose first and offer the
rest as a second pass.
