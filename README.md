# CandyCo Claude plugins

CandyCo's internal Claude Code plugin marketplace. Add it once and install the plugins your team needs. The first plugin here is the **CandyCo Design System** — the default visual language for every artifact, report, slide, and document we build with Claude.

## Install (one time, per person)

In Claude Code, run:

```
/plugin marketplace add candyco-plugins/claude-plugins
/plugin install candyco-design-system@candyco
```

That's it. The design system — tokens, fonts, logos, the report template, and the always-on design skill — is now bundled on your machine and applied automatically when you build anything visual.

> If `candyco-plugins/claude-plugins` is a **private** repo, make sure your machine is authenticated to GitHub first (`gh auth login`, or an SSH key with access to the `candyco-plugins` org).

## What's inside

| Plugin | What it does |
|--------|--------------|
| `candyco-design-system` | Loads the CandyCo design skill plus all bundled assets: `colors_and_type.css` tokens, the four brand font families, the official logos, the paged 8.5×11 report template, component specimens, and board-deck scaffolding. Applies by default to every visual artifact. |

## Updating

When the design system changes, we bump the plugin version and publish. To pull the latest:

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
