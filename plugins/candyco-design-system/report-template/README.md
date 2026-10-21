# Report template — paged 8.5×11 layout (v2)

The default layout for every CandyCo HTML report, briefing, analysis, recap,
or long-form document. This pattern is **the assumption** unless the user
explicitly asks for something else (a single scrolling page, a one-pager,
a slide deck, a raw markdown file, etc.).

## Two styles — pick by audience

| Style | Use for | Starter | `<body>` class | Masthead |
|---|---|---|---|---|
| **Internal** | Daily and weekly reports, ops and quality reports, internal analyses — the default | `template.html` | `style-internal` | Black rule, black logo, bold title. KPIs sit in section 02. |
| **Formal** | Board reports, board pre-reads, investor and partner reports, anything formal | `template-formal.html` | `style-formal` | Dark Shadow Grey band, white logo, the four headline KPIs inside the band. |

Board **slide decks** are a separate format — see `board-deck/`. The formal
report style is for written, paged board material.

Both styles share one stylesheet (`report.css`) and the same page structure,
so content moves between them by swapping the masthead, running head and
body class.

## Page structure

```
<body class="style-internal">            ← or style-formal
  <div class="doc-frame">
    <section class="sheet">               ← one 8.5×11 page
      <header class="masthead rule">…     ← cover only (.rule internal / .band formal)
      <div class="runhead rule">…         ← inner sheets instead of the masthead
      <div class="body">
        <div class="status-line">…        ← optional: Preliminary / Draft / Final
        <section class="sec">             ← numbered section
          <div class="rail">01 · title · hint</div>
          <div class="main">…content…</div>
        </section>
      </div>
      <div class="sheet-footer">[Doc title] · Page N of M</div>
    </section>
  </div>
```

- **Numbered left rail.** Every section is a `.sec` with a rail (Yeseva
  number, short title, optional one-line hint) and a main column. Numbers run
  continuously through the document (01, 02, 03 … across sheets), so anyone
  can say "look at section 05."
- **Logo in every cover header.** `candyco-logo-black.png` on the internal
  masthead, `candyco-logo-white.png` in the formal band. Never a text wordmark.
  Inner sheets carry the logo small in the running head.
- **Page-numbered footer on every sheet.** `[Doc title] · Page N of M`.
  Internal footers sit on a heavy rule in uppercase; formal footers are quiet
  and say "Confidential."

## Writing rules — concise, bullets, hierarchy

- **Bullets, not long sentences.** Every point or explanation is a short
  bullet in a `.points` list: one idea, number first, under ~15 words. No
  paragraphs of prose in the summary. If a bullet needs a second sentence,
  it is two bullets.
- **Lead with the one finding.** Use `<ul class="points lead">` for the
  summary; the first bullet renders larger. It is the single thing the reader
  should take away.
- **Bold the number, not the sentence.** `<strong>` goes on the figure and
  the item it belongs to.
- **Sentence case** for headings and labels. ALL-CAPS only for eyebrow-size
  labels (KPI labels, table heads, running head).
- **Concrete numbers.** Never "lots of" or "many" — always the count.
- **One accent per page.** Bars are grey; racing red marks the one flagged
  row (`tr.flag` + `.meter .hot`). Status capsules use semantic colors.
- **Hierarchy from weight and size**, not color. Body stays `--fg-1`.
- **No emoji. No cards, shadows, or side stripes** — structure comes from
  rules and the rail.
- **Lead with units (lbs, pieces, hours), follow with dollars** in
  operational reports.

## Components

| Component | Class | Notes |
|---|---|---|
| Summary bullets | `ul.points` / `ul.points.lead` | Square ink bullets. `.lead` enlarges the first item. |
| KPI row | `.kpis > .kpi` (`.l` label, `.v` value, `.s` sub) | Yeseva numbers, hairline columns. `.kpis.three` for three. Units in `<small>` after the value. |
| Table | `table` + `<colgroup>` widths | Fixed layout, black header rule, hairline rows, long text truncates with an ellipsis. `td.desc` greys descriptions, `td.wrap` allows wrapping, `.r` right-aligns, `tr.flag` bolds the row that matters, `tr.total` for totals. |
| Bar meter vs goal | `<div class="meter" style="--v:72.5;--g:80"><i></i><u></u></div>` | 0–100 scale. `<u>` is the goal tick. |
| Diverging bar | `<div class="meter div [neg] [over]" style="--v:73.1;--max:40"><i></i></div>` | Centered on zero/target. `--v` is the absolute value; add `.neg` for negatives and `.over` when past `--max` (draws an arrow). |
| Flagged bar | `<i class="hot">` | Racing red. One per table. |
| Status capsule | `span.cap.success / .warning / .error / .info / .neutral` | Short text labels ("On track," "Off goal"). |
| Key | `.key` | Two-column legend under a table: capsule, then meaning. |
| Status line | `.status-line` | Capsule + one line, above section 01. |
| Chart | `.main.chart` with a sized `<div><canvas></div>` + `.caption` | Grey series, red only for the one thing that matters. |
| Actions | `table.actions` (`td.no`, `td.owner`) | Numbered actions, owner, priority capsule, due date. |
| Sources | `p.sources` | One line of sources, one of method, one of confidence. |
| Wide table | `.sheet.landscape` + `table.appendix-wide` | See "Wide tables" below. |

### Retired in v2

`.hero`, `.stats/.stat`, `.goal-box`, `.audience-grid`, `.run-meta-strip`,
`.card`, `.cover-head`, `.meta-strip`, and `.lead` paragraphs are gone.
Use instead: the `.points.lead` first bullet (for `.hero`), `.kpis` (for
`.stats` and `.goal-box`), a meter with a goal tick (for goal framing), the
masthead meta + status line (for `.meta-strip` / `.run-meta-strip`), and a
`.sec` per team (for `.audience-grid`). Reports that vendor an older copy of
`report.css` — for example the ops portal's daily reports — keep rendering
with their copy until they are migrated.

## How to start a new report

1. **Pick the style** from the table above and copy `template.html` or
   `template-formal.html` to the project folder. Rename it.
2. **Copy the logo** the style uses into the same folder and point `<img src>`
   at the local file so it resolves when shared or printed.
3. **Inline the CSS** for portability (paste `colors_and_type.css` and
   `report.css` into a `<style>` block), or ship both files alongside.
4. **Replace placeholders.** Anything in `[brackets]` is a placeholder.
5. **Add or remove sheets** by duplicating `<section class="sheet">`. Inner
   sheets use the running head, not the masthead. Keep section numbers
   continuous and update every `Page N of M`.

## Avoiding print overflow

Every sheet is exactly 11in tall and clips anything past that. On screen a
dashed red line marks the bottom edge. **If content crosses the line, split
the sheet into two** — do not shrink fonts or padding below these defaults.

Content budget per sheet (main column, roughly):

| Sheet | Fits comfortably |
|---|---|
| Internal cover | Status line + 4-bullet summary + KPI row + one 6–8 row table |
| Formal cover | 4-bullet summary + one 6–8 row table (KPIs are in the band) |
| Inner sheet | Three sections: e.g. bullets + KPI row, a 10-row table, and a chart or actions table |

Pre-flight before delivering:

1. Open in Chrome and scroll every sheet — nothing crosses the dashed line,
   and the last section clears the footer.
2. Section numbers run 01 → N with no gaps; footers say `Page N of M`
   with the right M.
3. Exactly one flagged row (red bar) per table, at most one accent per page.
4. Print preview: Letter, portrait, 100% scale, **background graphics on**,
   browser headers and footers off.

## Wide tables on portrait pages

Every page prints as Letter portrait. Tables with more than ~10 columns go on
a `.sheet.landscape`: 14" wide on screen, and in print the content rotates -90°
to fit the portrait page (CSS landscape `@page` rules are unreliable across
browsers and print drivers). Wrap **all** the sheet's content, footer
included, in the two rotation divs:

```html
<section class="sheet landscape" style="--print-scale: 0.82;">
  <div class="print-rotated-region">
    <div class="print-rotated-inner">
      <h2>…</h2>
      <p>…</p>
      <table class="appendix-wide">…</table>
      <p class="caption">…</p>
      <div class="sheet-footer">…</div>
    </div>
  </div>
</section>
```

Set `--print-scale` from the table's row count so everything shrinks together:

```python
if rows <= 6:    print_scale = 1.0
elif rows <= 8:  print_scale = 0.82
elif rows <= 10: print_scale = 0.72
else:            print_scale = 0.62
```

`table.appendix-wide` supports grouped column heads (`th.ap-grouphead` over
`colspan` groups), `td.ap-input` (item code), `td.ap-desc` (description), and
`tr.totals`.

## Number formatting conventions

- Negative values in parentheses: `(1,234)` not `-1,234`
- Zero / missing data as em-dash: `—` (never `0`, `N/A`, or blank)
- Currency: `$1,234` positive, `$(1,234)` negative
- Percentages: always signed on variance columns (`+0.1%`, `-12.4%`)
- Tabular numerals are on by default for every table and `.num`

## When to skip this format

If the user says "raw," "markdown only," "one-pager," "quick draft," "no
branding," "dashboard," "slide," or asks for a non-paged HTML page, do not
force this template. Pick the right format for the ask.
