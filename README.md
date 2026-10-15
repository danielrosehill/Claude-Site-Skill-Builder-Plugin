# Site Skill Builder

Build a Claude Code plugin for a website by looking at the site in your own browser.
Observe the pages, propose a roster of skills, get them approved one by one, write
them so they survive a redesign, and keep them alive as the site drifts.

The default route is **your own signed-in Chrome**, via `claude-in-chrome` — so the
agent works inside the session you already have, no credentials are handled, and what
it sees is what you see. Headless Playwright/Puppeteer is the fallback for public
pages that need an unattended sweep; a plain fetch is used wherever it actually works.

> Built for sites you have an account with and the right to use with an agent. It does
> not bypass authentication, defeat bot challenges, or evade rate limits. It classifies
> every observation before it is committed, and it has a stop rule for the day a site
> map turns up something that looks like a vulnerability.

## The pipeline

| Skill | What it does |
|---|---|
| `site-recon-intake` | Target, page list or exploratory brief, account posture, constraints, robots/ToS |
| `pick-browser-route` | Own Chrome → headless → fetch; proves the route on one page first |
| `observe-page` | Walks the pages; writes an observation note per surface |
| `map-site-api` | Records the JSON endpoints worth depending on, with a canary field each |
| `propose-site-skills` | Ranked candidate roster — **stops for per-line approval** |
| `write-site-profile` | Every volatile fact in one JSON file |
| `author-durable-skill` | Writes an approved skill against the durability doctrine |
| `publication-gate` | Publishable / private / never-recorded, before every commit |
| `drift-probe` | Re-verifies routes, identity, handles and canaries; reports `CHANGED` |
| `repair-broken-skill` | Fixes what the site moved, and climbs the handle ladder while there |

Commands: `/site-plugin` runs the build, `/site-drift` runs the maintenance loop.

Agents: `skill-durability-auditor` (audits a draft for brittle handles and silent
failure paths), `observation-recorder` (writes up captured material, no browser).

## The two ideas it exists to enforce

**Durability.** A site skill is a bet that a page will look roughly the same next
month. Make the bet on URL grammar, the site's own JSON, structured data and
accessible names — never on generated CSS classes, list positions, or **pixel
coordinates**, which break on a window resize with the page unchanged. Assert page
identity before extracting anything, because the expensive bug in this domain is a 200
that serves someone else's content. Fail loudly; never return a partial result as if
it were complete. → `references/durability-doctrine.md`

**Publication discipline.** Most of what you learn mapping a site is ordinary
integration detail. A minority is the provider's defensive posture or a live weakness,
and that stays in a private workspace or is never written down at all. Every
observation is classified before it is committed. → `references/publication-policy.md`

## What it produces

A public plugin repo — `profiles/<site-id>.json`, skills, sanitised notes, a drift
probe — paired with a private dev workspace holding captures, account-bound material
and any findings. → `references/repo-layout.md`

## Neighbours

- **`browser-data-capture`** — owns the capture layer: HAR analysis, mitmproxy,
  live-tab observation, OpenAPI generation, per-domain maps, and `disclose-finding`
  for coordinated disclosure. Use it for the capture; this plugin decides what to
  build from it.
- **`create-plugins`** — scaffolds and registers the plugin repo itself. This
  plugin fills a repo; it does not create one.
- **`userscript-development`** — same browser-driven authoring shape, different
  artefact (Tampermonkey userscripts).

## Installation

```bash
claude plugins install site-skill-builder@danielrosehill
```

## License

MIT — see [LICENSE](LICENSE).
