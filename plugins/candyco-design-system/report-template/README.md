# Report template — paged 8.5×11 layout

The default layout for every CandyCo HTML report, briefing, analysis, dashboard
export, or long-form document. This pattern is **the assumption** unless the
user explicitly asks for something else (a single scrolling page, a one-pager,
a slide deck, a raw markdown file, etc.).

## What this gives you

- **Discrete pages.** Each `<section class="sheet">` renders as an 8.5" × 11"
  page on screen and prints as one page on Letter paper.
- **Logo lockup.** The cover header places the official `candyco-logo-black.png`
  at 38px height beside the document meta. White-background only — switch to
  `candyco-logo-white.png` if a sheet inverts to Shadow Grey.
- **Page-numbered footers.** Every sheet ends with `[Doc title] · Page N of M`.
- **Print-ready by default.** `@page` is set to Letter portrait at 0.5" margins.
  Browser print produces clean output with no extra setup.
- **Components ready to use.** Hero callout (light cream, print-safe), stat
  strip, capsules, audience grid, action-assignment table, chart card,
  footnote, **landscape sheet** for wide tables, **run-meta-strip** for context
  bands, **appendix-wide** dense numeric table, **goal-box** for KPI/threshold
  callouts, and **variance tinting** classes.

## Files

```
report-template/
├── README.md       ← this file
├── report.css      ← reusable stylesheet (imports colors_and_type.css)
└── template.html   ← starter HTML — copy and replace placeholders
```

## How to start a new report

1. **Copy `template.html` to your working folder** (e.g. the project folder
   under `/Users/SM/Documents/Claude/Projects/...`). Rename it.
2. **Copy the logo file(s)** the report uses to the same working folder so the
   image reference resolves when the file is shared or printed:
   ```
   cp "/Users/SM/Documents/CandyCo Design System/assets/logo/candyco-logo-black.png" .
   ```
   Update the `<img src>` to the local filename.
3. **Inline the CSS.** For maximum portability (so the file can be emailed and
   still render correctly), copy the contents of `colors_and_type.css` and
   `report.css` into a `<style>` block in the HTML. Otherwise, keep the
   `<link rel="stylesheet">` references and ship both CSS files alongside.
4. **Replace placeholders.** Anything in `[brackets]` is a placeholder.
5. **Add or remove sheets** by duplicating `<section class="sheet">…</section>`.
   Update the `Page N of M` numbers in every footer.

## Authoring rules (from the design system)

- **Sentence case** for all headings and buttons. ALL-CAPS only for eyebrows.
- **Concrete numbers.** Never "lots of" or "many" — always the count.
- **One accent per page.** Use a Four Candies color (emerald, steel-blue,
  golden-yellow, racing-red) sparingly to draw the eye to the one thing that
  matters. The hero block's racing-red accent on the headline is the typical
  move (golden-yellow on `.hero.dark` digital-only contexts).
- **Hierarchy from weight and size**, not color. Body copy stays `--fg-1`.
- **No emoji.** Status comes from semantic capsules (success / warning / error
  / info / neutral / dark).
- **Lucide icons** at 1.5px stroke, `currentColor`. Loaded from CDN in template.
- **Tables** use `font-variant-numeric: tabular-nums`; numeric columns use
  `class="num"`.
- **Lead with units (lbs, pieces, hours), follow with dollars** in operational
  reports. Pounds is the operational metric; dollars is the financial expression.

## Operational report patterns (added May 2026 from S'mores deep-dive)

Use these for production / scrap / KPI / variance reports:

- **`.hero`** is now the print-safe light-cream version by default. Use
  `class="hero dark"` only when the report is digital-only and the dark look
  is preferred. The light version forces `print-color-adjust: exact` so the
  hero renders identically in browser, print preview, and PDF.
- **`.sheet.landscape`** widens to 14"×8.5" — use when a table has more than
  ~10 columns or won't fit at 7.5pt portrait. Common pattern: appendix sheets
  for per-run / per-batch detail.
- **`.run-meta-strip`** is a context band above wide tables showing produced
  units, revenue, period, etc. Pairs naturally with `.appendix-wide`.
- **`table.appendix-wide`** is the dense reporting table format used by the
  cycle count / finance teams. Light-blue header band with optional grouped
  column heads (`th.ap-grouphead` over `colspan`-grouped columns), totals
  row uses `tr.totals`, key cells use `td.ap-input` (item code) and
  `td.ap-desc` (item description).
- **`.goal-box`** is the bold-bordered KPI callout that frames a result against
  an operational target. Three flex cells: two context numbers + one headline
  percentage with color band (`.goal-good` / `.goal-warn` / `.goal-bad`).
- **Variance tinting** — `td.pos` (green favorable), `td.neg` (amber small
  unfavorable), `td.neg-strong` (red bold large unfavorable).

### Number formatting conventions

- Negative values in parentheses: `(1,234)` not `-1,234`
- Zero / missing data as em-dash: `—` (never `0`, `N/A`, or blank)
- Currency: `$1,234` positive, `$(1,234)` negative
- Percentages: always signed on variance columns (`+0.1%`, `-12.4%`)
- Tabular numerals via `font-variant-numeric: tabular-nums` (already on `.num`,
  `.stat .num`, `.goal-value`)

## Print & screen behavior

- **On screen**, sheets stack as page-shaped white cards on a Shadow Grey 50
  background, each with a soft drop shadow. Designed for review and sharing
  via Cmd+P / "Save as PDF".
- **In print**, the screen chrome (background, shadows, doc-frame) is stripped
  via `@media print` rules. Each `<section class="sheet">` becomes one Letter
  page. Browser-set headers/footers should be turned off in the print dialog
  so the in-document `.sheet-footer` is the only footer that appears.

### Wide tables on portrait pages

Every page in a CandyCo report prints as Letter portrait. Wide content (e.g.
15-column appendix tables) is handled by **rotating the content -90°** via CSS
for print, not by switching the page to landscape. Reasons:

- CSS landscape `@page` rules are inconsistently respected across browsers and
  print drivers. Some print dialogs override them, others ignore them, and the
  user-facing experience is unpredictable.
- Rotating the content guarantees every printed page has the same orientation.
  The reader rotates the printed page (or tilts their head) 90° clockwise to
  read the wide table.

**Required HTML pattern.** Wrap **all** the rotatable content (including the
H2, intro paragraph, run-meta-strip, table, goal-box, caption, and the
sheet-footer) inside two wrapper divs in a `.sheet.landscape` section.
Everything inside rotates as one unit; the only thing outside the wrappers is
the section close. Set an inline `--print-scale` based on table row count so
all elements scale together when there are extra rows:

```html
<section class="sheet landscape" style="--print-scale: 0.82;">
  <div class="print-rotated-region">
    <div class="print-rotated-inner">
      <h2>Run X — Inventory Adjustments Detail</h2>
      <p>Window / context paragraph...</p>
      <div class="run-meta-strip">...</div>
      <table class="appendix-wide">...</table>
      <div class="goal-box">...</div>
      <p class="caption">...</p>
      <div class="sheet-footer">...</div>
    </div>
  </div>
</section>
```

On screen the wrappers are passthrough — children flow normally inside the
14"-wide landscape sheet for comfortable left-to-right reading. On print, the
`@media print` rules collapse the sheet to Letter portrait, the inner rotates
-90° around its top-left corner to fit a 7.5" × 10" rotation frame, and every
element's font-size + padding is computed via `calc(Npt * var(--print-scale))`
so all elements shrink together when more rows need to fit.

**Compute `--print-scale` based on table row count** in your build script:

```python
total_data_rows = ingredient_rows + 1 + pouch_rows  # +1 for totals row
if total_data_rows <= 6:    print_scale = 1.0
elif total_data_rows <= 8:  print_scale = 0.82
elif total_data_rows <= 10: print_scale = 0.72
else:                       print_scale = 0.62
```

Emit it on the section: `style="--print-scale: 0.82;"`. The CSS picks it up
and scales h2 13pt → 10.7pt, intro 9pt → 7.4pt, table 7pt → 5.7pt, goal-headline
20pt → 16.4pt, etc. — keeping the visual proportions while ensuring the rotated
content fits one portrait page.

**Print dialog tips for the user:**
- Use Chrome / Edge / Safari for best CSS transform support in print.
- In the print dialog: paper size **Letter**, orientation **Portrait**. Leave
  scaling at 100% (or "Default"). Every page prints as portrait.
- Turn **off** browser headers/footers (margins → Headers and footers checkbox)
  so the in-document `.sheet-footer` is the only footer that appears.
- "Background graphics" / "Print backgrounds" should be **on** so the hero
  block, table headers, and goal box render with their shading.

## When to skip this format

If the user says "raw," "markdown only," "one-pager," "quick draft," "no
branding," or asks for a non-paged HTML page (a dashboard, a single-screen
widget, a slide), do not force this template. Pick the right format for the
ask.
