# CandyCo Claude plugins

CandyCo's internal Claude Code plugin marketplace. Add it once and install the plugins your team needs. It holds the **CandyCo Design System** (the default visual language for every artifact, report, slide, and document we build with Claude) and **CandyCo MRP** (procurement's one-page MRP-by-finished-good report).

## Install (one time, per person)

In Claude Code, run:

```
/plugin marketplace add candyco-plugins/claude-plugins
/plugin install candyco-design-system@candyco
```

That's it. The design system — tokens, fonts, logos, the report template, and the always-on design skill — is now bundled on your machine and applied automatically when you build anything visual.

> If `candyco-plugins/claude-plugins` is a **private** repo, make sure your machine is authenticated to GitHub first (`gh auth login`, or an SSH key with access to the `candyco-plugins` org).

### Other plugins

Once the marketplace is added, install any plugin by name. For example, procurement's MRP report tool:

```
/plugin install candyco-mrp@candyco
```

> `candyco-mrp` reads live NetSuite data, so each person running it needs the **NetSuite connector enabled and authenticated** in their own Claude session.

## What's inside

| Plugin | What it does |
|--------|--------------|
| `candyco-design-system` | Loads the CandyCo design skill plus all bundled assets: `colors_and_type.css` tokens, the four brand font families, the official logos, the paged 8.5×11 report template, component specimens, and board-deck scaffolding. Applies by default to every visual artifact. |
| `candyco-mrp` | The `mrp-by-fg` skill: enter a finished-good item number and get a consolidated ~30-week MRP report (Excel + HTML) for every purchased component of its multi-level NetSuite BOM. Replaces the manual item-by-item "MRP Consolidated Report - Weekly Copy & Paste." Say **"run MRP Hack Report"** with an item number. |

## Updating

When any plugin changes, we bump its version and publish. To pull the latest for everything in this marketplace:

```
/plugin marketplace update candyco
```

## Maintaining this marketplace

- Plugins live under `plugins/<plugin-name>/`, each with a `.claude-plugin/plugin.json` manifest.
- The catalog is `.claude-plugin/marketplace.json` at the repo root.
- To ship a change to the design system: edit files under `plugins/candyco-design-system/`, bump `version` in that plugin's `plugin.json`, commit, and push. Teammates run `/plugin marketplace update candyco`.
- To add a new CandyCo plugin: create `plugins/<new-plugin>/.claude-plugin/plugin.json`, add an entry to `marketplace.json`, commit, push.

## Source of truth

The design system's working copy historically lived at `~/Documents/Claude OS/CandyCo Design System/` on Scott's machine. **This repo is now the canonical, shareable copy.** Edit here and publish; keep the local folder in sync or retire it.
