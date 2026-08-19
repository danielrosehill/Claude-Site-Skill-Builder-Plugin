# The durability doctrine

A site skill is a bet that a page will still look roughly the same next month. The
bet is never certain, so the goal is not "never breaks" — it is:

> **specific enough to be useful, general enough to survive a redesign of the parts
> you did not care about, and loud enough to tell you when it finally breaks.**

Silent wrongness is the failure mode that costs real money. A skill that stops
working and says so is a small maintenance task. A skill that keeps returning
plausible numbers from the wrong element is a wrong answer with a confident voice.

## The handle ladder

When a skill needs to find something on a page, prefer handles in this order.
Anything below rung 4 must be paired with a verification assertion (see below) and
recorded in the profile as fragile.

| # | Handle | Why it survives | Example |
|---|---|---|---|
| 1 | **URL grammar** | Routes are contracts; breaking them breaks inbound links and SEO | `/BL_{id}/{slug}`, `?keywords=` |
| 2 | **The site's own JSON endpoint** | Changes on a release cadence, not a design cadence; shapes are versioned in practice | `/api/dpc`, `/REST/KeywordSearchV2/Get` |
| 3 | **Structured data the site publishes about itself** | Exists for Google and analytics; nobody dares churn it | JSON-LD, `itemprop`, `og:` meta, `rel=canonical`, `__NEXT_DATA__`, `dataLayer` pushes |
| 4 | **Semantic / accessible handles** | Screen readers depend on them; changing them is a regression | `role`, accessible name, `<label>` text, `name=` on inputs, heading text |
| 5 | **Stable test hooks** | Put there deliberately to be stable | `data-testid`, `data-product-id` |
| 6 | **Structural landmarks anchored on visible text** | Survives restyling, not restructuring | "the table whose header row contains MODEL", "the section under the heading Specifications" |
| 7 | **CSS classes, nth-child, absolute XPath** | Generated, minified, reshuffled by the build | `.sc-1x2y3z`, `div > div:nth-child(4)` |
| — | **Pixel coordinates** | Never. Not a handle at all — see below | `click(612, 340)` |

Rung 7 is a last resort. Generated class names change when a designer touches an
unrelated component — they encode nothing about meaning.

## Never pixel positions

Coordinates are not a handle. A skill must never record, or act on, a screen position:
no "click at (612, 340)", no "the button 40px below the logo", no offsets measured off
a screenshot.

They break on everything that is not the page changing at all: a resized window, a
different zoom level, a scrolled viewport, a device-pixel-ratio difference, a cookie
banner that shifts the layout down, a font that renders a line taller, a sticky header
that appears on scroll. The page can be byte-identical and the coordinate still wrong.

This matters most when driving a real browser, because the click tool takes
coordinates and it is the path of least resistance. Do not take it:

- Locate the element **semantically** first — by role, accessible name, label text,
  link text, `data-testid`, or the text a person would read.
- Use the browser tooling that returns element references from a page read, and act on
  the reference, so the position is resolved at run time rather than baked in.
- Where a coordinate is unavoidable for one interaction (a canvas, a map, a drag),
  derive it at run time from the element's own bounding box, and record *the element*
  in the profile — never the number.
- Screenshots are evidence for a human, not a handle for a skill. If a skill's
  instruction can only be followed by looking at a picture, it is not a skill yet.

The same reasoning rules out other run-time-varying anchors: element indexes in a
list that reorders, "the third result", and anything keyed to viewport size.

## Write instructions a person could follow

Skills are executed by an agent that can *look at the page*, not by a parser. So
describe the target the way you would describe it to a colleague over the phone:

> Find the price table — the one whose header row reads PRICE PER CARTON. Read the
> row whose MODEL cell matches the model number you were given.

That instruction survives a redesign that moves the table, renames its class,
changes its border, or wraps it in a new container. A CSS selector survives none of
those. When you do record a selector, record it as *a hint that was true on
<date>*, not as the definition of the target.

## Always assert page identity before extracting

The most expensive bug in this domain is the page that answers 200 with somebody
else's content. Real, observed cases:

- A numeric ID resolves and the slug after it is decorative, so a stale or guessed
  slug silently serves a different product.
- An anti-bot challenge returns **HTTP 200** with 1.8 KB of markup; a parser reads
  zero results and reports "no matches", which is indistinguishable from a real
  empty result set.
- A logged-out session returns the login page at 200 under the requested URL.
- An SPA shell returns 200 before hydration, with none of the data in the DOM.

So every extraction skill opens with an identity check, and fails loudly if it does
not pass:

1. Compare `rel=canonical` (or the final URL after redirects) with what was asked.
2. Compare the page's own title / `<h1>` / echoed identifier with the input.
3. Classify the body before parsing: real page, challenge, login wall, empty shell,
   error page. Never infer success from the status code.

## Fail loudly, never partially

Every skill states its **breakage signature**: what it says when the site has moved.

- Say `CHANGED: <what was expected> not found at <where>` and stop.
- Never return a partial extraction as if it were complete.
- Never fall back to "best guess from the text" without labelling it as such.
- Exit non-zero from scripts so a caller cannot mistake it for an empty result.

## Isolate the volatile parts

Put everything that will age in **one file** — the site profile JSON. Selectors,
endpoint paths, URL templates, the verification date. Prose in a SKILL.md should
describe *method*; the profile carries *facts*. When the site changes you edit one
JSON file and every skill follows, instead of grepping six markdown files for a
class name.

## Anti-patterns, each learned the hard way

- **Counting things.** "The nav has 37 categories" is a fact with a shelf life of
  one merchandising meeting.
- **Currency-anchored regexes.** Tables often print the symbol on the first row
  only; a `$`-anchored pattern finds one price and reads as a page with one price.
- **Cell index as column index.** `rowspan`/`colspan` mean a shared cell is omitted
  on following rows. Expand spans before reading a table by position.
- **Assuming one block per page.** Two price charts, two variant tables, two
  "add to basket" forms — plural is the safe default.
- **Baking in the user's own account state.** Contract pricing, saved addresses,
  A/B buckets and locale all vary by session. Note what was observed *under this
  account* and say so.
- **Pixel positions or screenshot offsets.** See above — the most brittle handle
  there is, and the easiest to reach for when driving a live browser.
- **Encoding a defence.** Skills describe what to do for the user, not what the
  site checks. See `publication-policy.md`.

## Every skill carries provenance

At the bottom of each generated SKILL.md:

```markdown
## Provenance

Observed on <YYYY-MM-DD> from <page-note-path>. Handles used: <rung numbers>.
Fragile: <any rung 6–7 handle>. Re-verify with `drift-probe`.
```

That line is what makes the next agent — with no memory of this session — able to
tell a stale skill from a current one.
