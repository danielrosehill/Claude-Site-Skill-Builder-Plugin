# <Surface name> — <what this page is for>

- **URL pattern:** `<https://host/path/{id}>`
- **Route used:** `<claude-in-chrome | playwright | fetch>`
- **Session required:** `<yes | no>` — `<what differs when signed out>`
- **Observed:** `<YYYY-MM-DD>`
- **Unit of the page:** `<one product | one variant | a family | an order line>`

## Identity check

How to confirm this is the page that was asked for:

- Canonical / final URL: `<what it should be>`
- Title or `<h1>`: `<what it should contain>`
- Echoed identifier: `<where the input appears back on the page>`
- Failure modes seen: `<slug ignored | login wall at 200 | unhydrated shell | challenge>`

## Data on this page

### <data point>

- **Find it:** `<how a person would describe locating it>`
- **Rung:** `<1–7 per the durability doctrine>`
- **Selector hint (`<YYYY-MM-DD>`):** `<selector, as a hint only>`
- **Assert:** `<what proves the right element was found>`
- **Traps:** `<repeated blocks, spanned cells, first-row-only symbols, locale>`

## Interactions

Described as elements, never as positions:

- `<action>` — the element whose `<role / accessible name / label>` is `<...>`

## Not on this page

- `<stock | freight | delivery date | tax treatment>` — `<where it actually lives, if known>`

## Observed vs inferred

- Observed: `<...>`
- Inferred, not checked: `<...>`

## Private material

`<none | moved to the private workspace: what and why>`
