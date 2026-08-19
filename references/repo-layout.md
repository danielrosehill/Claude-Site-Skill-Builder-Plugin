# What a site plugin looks like

Two repositories, one public and one private. The split is the publication policy
made structural: it should be impossible to leak a capture by writing to the wrong
directory without noticing.

## Public — the plugin

```
Claude-<Site>-Plugin/
├── .claude-plugin/plugin.json
├── profiles/<site-id>.json        # the volatile facts, one file
├── skills/<skill-name>/SKILL.md   # the approved skills
├── commands/                      # thin front doors, optional
├── reference/
│   ├── url-taxonomy.md            # how the site's routes are shaped
│   └── access-routes.md           # what reaches it, as plain fact
├── scripts/probe.py               # drift probe (optional but recommended)
├── notes/                         # sanitised observation notes
├── README.md
└── LICENSE
```

## Private — the dev workspace

Sibling repo, private, named `<Site>-Plugin-Dev`, or an existing private research
workspace:

```
<Site>-Plugin-Dev/
├── captures/          # HAR, saved DOM, screenshots — gitignored from the public repo
├── notes/private/     # defence observations, unlinked endpoints, account-bound data
├── findings/          # incidental security findings + disclosure records
└── README.md          # says plainly that nothing here is publishable
```

Create it with `browser-data-capture:init-private-repo` if that plugin is installed —
it already scaffolds this shape and registers the path.

## Notes

An observation note per page or per surface, in `notes/`, named for what it covers:
`notes/product-detail.md`, `notes/search-results.md`. Written for an agent opening the
repo cold: what the page is for, what data is on it, which handles were used, what was
checked, what was assumed, the date.

Templates: `templates/observation-note.md` in this plugin.

## Where this plugin's outputs go

`site-skill-builder` writes into **the plugin repo you are building**, resolved from
`$CLAUDE_PROJECT_DIR` — it keeps no state of its own. If the target repo does not
exist yet, `create-claude-plugins:new-claude-plugin` scaffolds and registers it; this
plugin fills it.
