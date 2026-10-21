---
name: candyco-design
description: CandyCo's design system — colors, typography, spacing, voice, components, and assets. This is the DEFAULT visual language for every artifact, widget, HTML page, slide deck, dashboard, document, mock, or any visual output created for CandyCo unless the user explicitly says otherwise. Apply automatically whenever building any visual artifact, even if the user does not name the design system. ALSO apply whenever drafting a response to a customer complaint — e.g. "respond to a Costco complaint," "consumer complaint investigation," "complaint response," "answer this complaint from Hershey / Sam's Club / Trader Joe's," or any request to write back to a retail or brand customer about a complaint — and start from complaint-response-template/template.html. Skip only when the user signals "raw," "no branding," "quick sketch," or similar.
user-invocable: true
---

# CandyCo Design System

This skill ships as part of the `candyco-design-system` plugin. All design files — tokens, fonts, logos, templates, specimens — are bundled with the plugin and live at the plugin root, available as the environment variable `${CLAUDE_PLUGIN_ROOT}`.

**Resolve the root once at the start:** run `echo $CLAUDE_PLUGIN_ROOT` to get the absolute path, then read files relative to it (e.g. `${CLAUDE_PLUGIN_ROOT}/README.md`, `${CLAUDE_PLUGIN_ROOT}/colors_and_type.css`). Every path below is relative to that root.

This skill is the always-on default for artifacts. When invoked (explicitly or by default), read `README.md` for content fundamentals and visual foundations, then use the tokens and assets below.

## Quick map

- `README.md` — content fundamentals (voice, tone, casing), visual foundations (color, type, spacing, motion, layout, iconography), caveats.
- `colors_and_type.css` — canonical CSS variables and `@font-face` declarations. Source of truth for tokens. Copy this file into artifacts or `@import` it directly when feasible.
- `fonts/` — Assistant (sans, UI), Frank Ruhl Libre (editorial serif), Yeseva One (display), Minion Pro (legacy).
- `assets/logo/` — `candyco-logo-black.png` (dark on light), `candyco-logo-white.png` (light on Shadow Grey), `candyco-mark.jpg` (wordless mark for tight spaces). **Place the logo in the cover header of every report — never substitute with a text wordmark.**
- `assets/icons/` — Lucide iconography reference. Lucide icons are CDN-linked, 1.5px stroke, `currentColor` only.
- `preview/` — specimen cards for every token group. Useful as cookbook examples.
- `report-template/` — **default layout for every HTML report.** Paged 8.5×11 sheets, numbered left-rail sections, Yeseva KPI numbers, bar-meter tables, concise bullets. Two styles: `template.html` (internal — daily/internal reports, black-rule masthead) and `template-formal.html` (formal — board and formal reports, dark band). Always start here for reports, briefings, analyses, and long-form documents.
- `complaint-response-template/` — **standard written response to a retail or brand customer about a consumer complaint investigation.** 4-page customer-facing report (identification + traceability, containment, investigation evidence, root cause, CAPA) plus two internal guidance pages that are deleted before sending. Start from its `template.html` whenever the quality team responds to a customer complaint.
- `ui_kits/marketing-site/` — JSX components and a working `index.html` showing the system in production layout.
- `board-deck/` — board deck reference materials and reusable deck-stage scaffolding.

## How to use this skill

1. If the user has asked for a visual artifact (HTML page, dashboard, slide, mock, doc), apply this design system by default.
2. Read `README.md` first for the content and visual rules.
3. **For HTML reports, briefings, or analyses, default to `report-template/`** — paged 8.5×11 sheets with the logo lockup, page-numbered footers, and the standard component library. Read `report-template/README.md` and copy `report-template/template.html` (daily and internal reports) or `report-template/template-formal.html` (board and formal reports) as the starting point. Write points and explanations as short bullets, not long sentences. Skip only if the user signals "raw," "single page," "one-pager," "no branding," or asks for a non-paged format.
4. Pull tokens from `colors_and_type.css` rather than redefining colors, type, spacing, radii, or shadows ad hoc.
5. Use logos and fonts from this plugin. **Place `candyco-logo-black.png` in the cover header of every report** (or `candyco-logo-white.png` on inverse Shadow Grey backgrounds). Copy the logo file and any referenced fonts into the artifact output folder so the relative path resolves when the file is shared or printed.
6. Apply the voice rules from `README.md` to all copy: sentence case, "we/you," concrete numbers, no emoji.
7. If the user invokes this skill without other guidance, ask what they want to build, ask the right clarifying questions, then deliver as either an HTML artifact or production code.

## When to skip

If the user says "raw output," "no styling," "quick sketch," "unbranded," or similar — skip the design system and produce something fast and unstyled.

## Report components — v2 pattern library

`report-template/report.css` (v2) covers both report styles. Set `<body class="style-internal">` or `<body class="style-formal">`. Full table in `report-template/README.md`.

- **Masthead** — `.masthead.rule` (internal: black rule, black logo) or `.masthead.band` (formal: Shadow Grey band, white logo, KPI row inside the band). Inner sheets use `.runhead.rule` / `.runhead.band`.
- **Numbered section** — `.sec` with `.rail` (`.n` number, `.t` title, `.h` hint) and `.main`. Numbers run continuously across the document.
- **Summary bullets** — `ul.points.lead`: one idea per bullet, number first, under ~15 words; the first bullet is the headline finding.
- **KPI row** — `.kpis > .kpi` with `.l` / `.v` / `.s`. Yeseva numbers between hairlines.
- **Bar meters** — `.meter` (fill vs goal tick, `--v` / `--g`) and `.meter.div` (diverging around zero, `--v` / `--max`, `.neg`, `.over`). Grey bars; `.hot` + `tr.flag` on the one row that matters.
- **Capsules, key, status line, actions table, sources** — `.cap.*`, `.key`, `.status-line`, `table.actions`, `p.sources`.
- **Wide tables** — `.sheet.landscape` with the `print-rotated-region` / `print-rotated-inner` wrappers and `table.appendix-wide`; set `--print-scale` from row count. See `report-template/README.md`.
- **Variance tinting** — `.pos`, `.neg`, `td.neg-strong` on comparison cells.
- **Retired in v2:** `.hero`, `.stats`, `.goal-box`, `.audience-grid`, `.run-meta-strip`, `.card`, `.cover-head`, `.meta-strip`.

## Number formatting conventions for reports

Every operational/finance report should follow these conventions so the output reads consistently with what the cycle-count and finance teams produce:

- **Negative values** in parentheses: `(1,234)` not `-1,234`
- **Zero or no data** as em-dash: `—` (never `0`, `N/A`, or blank cells in numeric columns)
- **Currency** with $-prefix: positive `$1,234`, negative `$(1,234)`
- **Percentages** always signed on variance columns: `+0.1%`, `-12.4%`
- **Column alignment** uses tabular numerals: `font-variant-numeric: tabular-nums` (on by default for every table and `.num`)
- **Lead with lbs (or units), follow with dollars** in operational reports — pounds is the operational metric; dollars is the financial expression of the same data

These conventions live in code (formatting helpers, not CSS), but are documented here and at the bottom of `report-template/report.css` so every future report uses the same helpers.

## How to extend

This is a living system. The canonical copy lives in the `candyco-plugins/claude-plugins` repo under `plugins/candyco-design-system/`. To change the system, edit the files there and publish a new version (bump `version` in `.claude-plugin/plugin.json`), then have the team run `/plugin marketplace update candyco`. Edit locations:

- Tokens → `colors_and_type.css`
- Rules and voice → `README.md`
- Components → `ui_kits/`
- Specimens → `preview/`
- Report layout / paged-document defaults → `report-template/`
- Assets → `assets/`
