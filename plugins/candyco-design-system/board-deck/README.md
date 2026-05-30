# Board Deck — CandyCo board-presentation style

> The canonical layout + visual language for any CandyCo board deck.
> Use this every time a new deck spins up. Don't reinvent — extend.

This folder is the canonical home of the **Board Deck Style** — the
aesthetic established for the **May 28, 2026 Pure Foods · Pondera ·
Promus board meeting** deck and locked in afterward. New decks default
to this style; deviation is a deliberate decision, not a starting
point.

---

## What's in here

```
board-deck/
├── README.md                ← you are here
├── board-deck-style.css     ← the canonical stylesheet (import this)
├── live-tables.css          ← live-HTML financial-table system (drop in when the deck has P&L / BS / projections)
├── template.html            ← minimal starter, drop-in to spin up a new deck
├── colors_and_type.css      ← tokens (mirrors the root colors_and_type.css)
├── deck-stage.js            ← legacy custom-element runtime (used by older deck files; not required for the new style)
├── assets/                  ← brand assets (logo PNGs, etc.)
├── fonts/                   ← embedded Google-Fonts fallbacks
└── CandyCo Board Deck.html  ← v1 archive — predates the Board Deck Style; kept for reference, do not author against this
```

To start a new deck:

1. Copy `template.html` into a new working folder.
2. Update the `<title>`, the chrome-top deck-identifier text, the
   slide-title text on each `<section class="slide">`, and the page
   numbers in chrome-bottom.
3. Drop the brand assets (or the CandyCo Design System `assets/`
   folder) alongside, so `assets/candyco-logo-black.png` and
   `assets/candyco-logo-white.png` resolve.
4. Author content slides inside `<section class="slide" data-section="…">`
   where `data-section` is one of: `financial`, `operations`, `sales`,
   `capacity`, `fsqa`, `customer`, `plant`. These trigger the
   light-canvas treatment. Cover, agenda, section dividers, and
   closing use `data-section="cover"` / `data-section="agenda"` and
   stay on the dark canvas.
5. `@import` or `<link>` to `board-deck-style.css` for the visual
   pattern. Don't rewrite — extend with a deck-specific stylesheet
   if you need new components.

---

## The Style at a glance

### Two-theme split

- **Dark slides** — Cover, agenda, section dividers, closing.
  Shadow Grey 900 canvas, ivory type, copper editorial chrome (eyebrow
  + slide rule), faint ghost wordmark watermark anchored bottom-right.
  This is the **only** place copper appears in text.
- **Light slides** — every content section (Financial, Operations,
  Sales, Capacity, FSQA, etc.). Cool-grey `#F2F2F4` canvas, white
  cards lifted via soft shadow, white title bar at top, white footer
  bar at bottom, no copper text anywhere.

### Light-slide anatomy

```
┌────────────────────────────────────────────────────────────┐
│ [logo] Board Deck · May 28, 2026          Section · I    │ ← white title bar
│ Slide title — large, dark navy.                            │   (chrome-top + slide-header,
│                                                            │    border-bottom hairline)
├────────────────────────────────────────────────────────────┤
│                                                            │ ← grey body canvas
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │   floating white cards
│   │ • KPI 1  │  │ • KPI 2  │  │ • KPI 3  │  │ • KPI 4  │   │   live here
│   │   $75M   │  │   $14M   │  │   $8.5M  │  │   12.5M  │   │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                            │
│   ┌────────────────────────────────────────────────────┐   │
│   │ [TAG]  Card title                                  │   │
│   │ ─────────────────────────────────────────────────  │   │
│   │ data rows…                                         │   │
│   └────────────────────────────────────────────────────┘   │
│                                                            │
├────────────────────────────────────────────────────────────┤
│ Confidential · Internal use only                   05 / 31 │ ← white footer bar
└────────────────────────────────────────────────────────────┘
```

### Cards

- White (`#FFFFFF`) background. No tint.
- 14px corner radius.
- Soft two-layer shadow: `0 1px 3px @0.06 / 0 12px 32px @0.08` in
  the Shadow Grey 900 tint. Reads as paper-on-paper, not UI button.
- **No accent stripes — top, left, or otherwise.** Every card is
  the same neutral object; meaning lives in the data inside.

### Color discipline on light slides

- **Emerald** — favorable, above goal, better than budget.
- **Racing red** — unfavorable, below goal, worse than budget.
- **Neutral grey** — at-target, informational, no signal.
- **Golden yellow** — used only as the tag-chip background for
  categorical labels inside table eyebrows.
- **Copper** — **not in text** on light slides. Reserved for the
  dark-slide editorial chrome.

### Status dots

A small leading `<span class="dot fav|unfav|neutral"></span>` on
every KPI label, op-metric label, and notable customer row. The
single quiet color signal that replaces the abandoned colored
top-stripes.

### Yellow tag chip

`<span class="tag-chip">P&L</span>` style. One tag per panel
eyebrow at most. Use it to label what a card is (e.g., the table
inside is the P&L cost-driver detail). Never as decoration.

---

## Type

- **Yeseva One** — display, slide titles. The brand's loudest typographic move.
- **Frank Ruhl Libre** — editorial serif italic, used for the
  `<span class="ital">` clause inside a slide title and for the
  budget-vs-actual footnote text.
- **Assistant** — UI, body, tables, labels, chrome text.
- Tabular nums on every number column: `font-variant-numeric: tabular-nums`.

Sentence case for titles. ALL-CAPS only for eyebrows / tag chips,
tracked-out (`letter-spacing: 0.18em`).

---

## Reference deck

The May 28, 2026 board deck (see `Claude Work Projects/Capacity
Dashboard - 5.28.26 Board Deck/`) is the canonical reference
implementation. Every pattern documented here is in service to
that deck.

---

## What changed vs. v1 (`CandyCo Board Deck.html`)

v1 (April 2026) used:
- Ivory `#F5F2EC` panel fill on the white canvas
- 8px card radius
- Colored top-edge accent stripes per KPI (blue / gold / green / copper)
- Copper text for slide-eyebrow, year-group headers, tier rows, total rules
- Chrome positioned absolute in the slide corners

Board Deck Style (May 2026) flipped all of these:
- Cool-grey `#F2F2F4` canvas, white panels lifted by shadow
- 14px card radius, deeper shadow
- No accent stripes — every card is the same neutral object
- No copper text on light slides
- Chrome flows in the slide layout (chrome-top + slide-header form the
  title bar at top; chrome-bottom is the footer bar at bottom)

v1 is archived in place for reference but should not be the starting
point for new decks.

---

## Live HTML tables (financial slides)

Financial pages — P&L, balance sheet, projections, covenant
compliance — render as **live HTML tables inside a floating white
card**, not as screenshots of an Excel export. Tables are searchable,
print as crisp text, and update whenever the underlying workbook
changes (regenerate via the generator-script pattern below).

The canonical CSS lives in `live-tables.css`. Import it alongside
`board-deck-style.css`:

```html
<link rel="stylesheet" href="board-deck-style.css">
<link rel="stylesheet" href="live-tables.css">
```

### Anatomy

```html
<div class="slide-body reveal" data-d="4">
  <div class="pl-embed pl-pnl">      ← modifier picks the fit
    <div class="pl-card">             ← white floating card
      <table>
        <colgroup>…</colgroup>
        <tr class="ghead">…</tr>      ← top group headers (pill chips)
        <tr class="shead">…</tr>      ← $ / % Net Sales / $ / Lb sub-headers
        <tr class="sp">…</tr>         ← spacer
        <tr>…</tr>                    ← data row
        <tr class="b rt">…</tr>       ← bold subtotal w/ top rule
        <tr class="b rt rd">…</tr>    ← grand total w/ top rule + double rule
      </table>
    </div>
  </div>
</div>
```

The `.slide` must declare `container-type: inline-size` (it does, via
the rule in `board-deck-style.css` §10). That enables the `cqi`
font-clamp inside the table to scale with slide width.

### Which modifier to use

| Modifier   | Columns | Width fill | Typical use                                          |
|------------|---------|-----------:|------------------------------------------------------|
| (default)  | 12–15   | natural    | Wide P&L tables (Actual + Budget + PY + 2 variances) |
| `.pl-bs`   | 5–7     | 64%        | Balance sheet (quarterly close columns)              |
| `.pl-pnl`  | 9       | 82%        | P&L split into vs-budget / vs-prior-year             |
| `.pl-fp`   | 13–14   | edge-to-edge | Financial projections (monthly + quarter-end)      |

All four hit ~85–95% height fill at 1080p with zero clipping. The
modifier exists because each table has a different column count,
and a single one-size-fits-all font clamp leaves the narrow tables
swimming in the middle of the page.

### Cell classes

Defined once in `live-tables.css` and used by every variant:

- `.lbl` — first column, left-aligned row label
- `.num` — right-aligned tabular-nums number
- `.d` — adds a leading `$` via `::before`
- `.g` — group gap, extra left padding (first cell of each col group)
- `.b` — bold (apply to `<tr class="b">` on subtotal rows)
- `.serif` — Times serif (used on adjustments below EBITDA)
- `.rt` / `.rb` / `.rd` — top / bottom / double-bottom rule
- `.sp` — spacer row
- `.ghead` / `.shead` — group-header / sub-header rows
- `.ul` — underline (inside `.shead`, for month-column headers)
- `.psec` — section divider row (INCOME STATEMENT / BALANCE SHEET /
  COVENANTS in the projections table)
- `.comp` — covenant compliance flag, renders "YES" in emerald-deep
- `.blue` — CandyCo blue, used for Pounds Sold / Pounds Produced
  and Operating Metrics rows

### P&L split convention (vs Budget / vs Prior Year)

For the **simplified "Pure's View" P&L**, the table splits across
two adjacent slides. The source workbook itself is laid out as two
blocks; the slide split mirrors that structure exactly:

- **Slide N — "YTD P&L detail — vs budget, [Month YYYY]."**
  9 columns: spacer + 2026 Actual ($, %NS, $/Lb) + 2026 Budget ($,
  %NS, $/Lb) + Variance to Budget ($, %Var).

- **Slide N+1 — "YTD P&L detail — vs prior year, [Month YYYY]."**
  Same 9 columns; Budget swapped for Prior Year and Variance to
  Budget swapped for Variance to Prior Year.

Both slides share the **same row set** (Pounds Sold → Net Revenue →
COGS components → Gross Margin → opex → Net Income → EBITDA →
Adjusted EBITDA) and both keep the **Operating Metrics block**
(Production $, Materials & Packaging % of Sales, Direct Labor %
of Production, Scrap % of Production) at the bottom.

The detailed standard-costing P&L still lives untouched in **Exhibit
B (vs budget detail)** and **Exhibit C (YOY detail)** in the
appendix.

### Generator-script pattern

Live tables are generated, not transcribed. The pattern:

1. Place the source workbook in `Data Sources/` alongside the deck
   (e.g. `5.28.26/Data Sources/Simplified P&L Pages - Pure's View.xlsx`).
2. Write a small Python script in `/tmp/` using `openpyxl` that reads
   the workbook and emits the table rows as HTML with the cell
   classes above. Define formatters for `money()` (round to $000s,
   commas, parens for negatives), `pct()` (×100 to 1 decimal), and
   `perlb()` (2 decimals, `-` for zero).
3. Splice the generated `<table>` element into the slide via a second
   Python script anchored on a unique substring inside the slide
   section.
4. Verify the generated values cross-foot (Gross Margin = Net Revenue
   − COGS, Total Assets = Total Liabilities & Equity, etc.) before
   declaring done.

The 5.28.26 deck has working examples for all three table types:
- Balance sheet: `BS Data for Board Deck.xlsx`
- Projections: `Financial Projections.xlsx`
- Simplified P&L: `Simplified P&L Pages - Pure's View.xlsx`

---

## Status chips (bite chips)

Use `.bite-chip` for one-token state labels on rows, cards, or
opportunity tiles. The three flavors are semantic — don't invent new
colors for state.

```html
<span class="bite-chip live">Live</span>
<span class="bite-chip ready">Bench candidate</span>
<span class="bite-chip dev">Future</span>
```

| Class     | Means                                              | Color        |
|-----------|----------------------------------------------------|--------------|
| `.live`   | In market today, committed, approved, awarded      | Emerald solid |
| `.ready`  | Ramping, in trial, "bench candidate"               | Steel-blue tint |
| `.dev`    | Future, TBD, waiting on a decision, in development | Golden-yellow solid |

When labelling a cold-press bite that's bench-ready, use
`"BENCH CANDIDATE"` (not `"bench-ready"`) — locked in by the
5.28.26 deck.

---

## Page numbering

- Each content slide has a `<span class="page-num">NN / TT</span>`
  inside `chrome-bottom`. NN is zero-padded.
- The title slide (slide 1) does **not** carry a page number.
- Content slides number 02 → TT contiguously, no gaps.
- **Appendix exhibits** use **text labels**, not numbers:
  `<span class="page-num">Exhibit A</span>`, `Exhibit B`, `Exhibit C`.

**Inserting a slide.** If you anticipate adding a slide later, leave
a numeric gap in the page-num sequence (e.g. skip 07) and set TT to
the post-insert count. When you fill the gap, you only renumber the
single slide that absorbs the shift. The 5.28.26 deck used this
pattern to insert the prior-year P&L slide cleanly.

**Renumbering a closed deck.** Do high-to-low string replacements
(`33 / 34` → `34 / 34`, then `32 / 34` → `33 / 34`, …) to avoid
collisions. Update the `SLIDE NN` HTML comments to match.

---

## Appendix structure (5.28.26 reference)

Three exhibits sit after the main deck, all numbered with text
labels:

- **Exhibit A — Bridge detail.** Bar-by-bar waterfall of the 2025 →
  2026 budget bridge. Kept as a static `<img class="appendix-img">`
  because the visual shape (waterfall) is the message, not the cell
  grid.
- **Exhibit B — P&L vs budget detail.** The original detailed
  standard-costing P&L (Cost of Sales at Standard, Material
  Variances, Shipping Materials, Freight In, Inventory Usage,
  Direct Labor, Variable / Fixed Overhead, Freight Out). Lives here
  in full so the simplified main-deck P&L can stay simple.
- **Exhibit C — P&L YOY detail.** Same detailed structure, prior-year
  comparison.

Exhibits are linked from the main slides via small "View Detail →"
chips when the main slide presents a summary that the exhibit
expands.

---

## What's locked in (the "no" list)

These were tried and explicitly rejected during the 5.28.26 build.
Don't re-introduce them in new decks without a deliberate decision:

- **No copper accent tinting on light-section cards.** Cards are
  pure white. Copper stays on the dark slides only.
- **No green / red gradients on tailwinds / headwinds cards.** Plain
  white cards; the headwind/tailwind framing is the structure.
- **No emoji in deck UI.** Status comes from semantic color tokens
  (emerald / racing-red / golden-yellow) and the chip system.
- **No accent stripes on KPI cards.** Every card is the same neutral
  object; the data is the signal.

---

## Reference deck stats (5.28.26)

- 34 slides total (title + 02–34 + Exhibits A/B/C)
- Sections: I · Financial update · II · Operations · III · Sales ·
  IV · Capacity & capital · Closing
- Lives at:
  `/Users/SM/Library/CloudStorage/OneDrive-Mrs.Call'sCandyCompany/Documents/Sales Team/4. Strategy/Board Meeting/2026/5.28.26/5.28.26 CandyCo Board Deck.html`
- Data sources subfolder: `5.28.26/Data Sources/`
- Asset folders: `assets/sales/`, `assets/sales-draft/`
