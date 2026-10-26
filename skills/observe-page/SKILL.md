---
name: observe-page
description: Observe one page or a list of pages in the browser and write an observation note — what data is there and which durable handles reach it.
---

# Observe a page

Turns a page into a note another agent can build a skill from without reopening the
browser. Read `references/durability-doctrine.md` first; it defines the handle ladder
this skill applies.

## Inputs

One or more URLs, and what the user wants from each page. With no URL list, take the
page list from `notes/brief.md`, which is either the user's own list or their picks from
`survey-site-surface`.

## Steps

For each page, in sequence, at the pace in `references/anti-bot-posture.md`. Never
fan out parallel loads against a live site:

0. **Start network capture before loading** (`references/network-discovery.md`),
   in the same tab you will keep using. Afterwards, list the data calls the page made
   and which on-screen values each one carries. If a call carries the data, that is
   the handle (rung 2) and the markup is the fallback. Pass the calls to
   `map-site-api`.
1. **Load it on the chosen route** and confirm identity: final URL after redirects,
   `rel=canonical`, title, and any identifier echoed back. Note any mismatch — a
   numeric id whose slug is decorative will serve a different item at 200.
2. **Read the page as a person.** What is this page for, what does it answer, what is
   the unit of the thing on it (a product, a variant, a family, an order line)?
3. **Find the data at the highest rung available.** Check, in order: JSON-LD and
   microdata, `og:`/meta tags, embedded state (`__NEXT_DATA__`, `dataLayer`,
   hydration payloads), then accessible names, labels and heading-anchored structure.
   Record the rung, not just the result.
4. **Write the durable description** of each data point — how a person would tell a
   colleague to find it. Record any CSS selector as a dated hint beneath it, never as
   the definition.
5. **Record the assertion** that proves the right element was found (the model cell
   matches the requested model; the heading names the requested order).
6. **Record what is not on the page.** Stock, freight, delivery date, tax treatment —
   whatever a caller will assume is there and isn't.
7. **Note the traps**: repeated blocks, `rowspan`/`colspan`, symbols printed on the
   first row only, values that differ when signed in, anything locale-dependent.
8. **Record interactions as element descriptions**, never as positions. If a skill
   will have to click something, note what the element is called and how a person
   would identify it — never a coordinate, an offset, or "the third button".
9. **Classify every line** against `references/publication-policy.md` as you write it.
   Account-bound values and defence observations go to the private workspace.
10. **Watch the session.** If identity drops mid-walk (login redirect, 401 on a data
    call), stop and follow `session-keepalive`. Don't record a login page as the
    observation.

## Output

`notes/<surface>.md` in the target repo, from `templates/observation-note.md`, with
today's date. Batch write-ups can be delegated to the `observation-recorder` agent —
hand it the captured text; it does not drive the browser.
