# CandyCo Design System

> **Industrial confectionary, dressed sharp.**
> A design system for CandyCo — a full-scale confectionary manufacturing partner that private-labels for America's biggest retailers (Costco, Sam's Club, Trader Joe's, Kroger, Walmart, Albertsons).

This is a **B2B operations brand**, not a consumer candy brand. CandyCo's customers are merchandising teams, supply-chain planners, and retail buyers — people who care about throughput, lead times, and capacity utilization. The design language reflects that: a near-black "Shadow Grey" primary anchors the system, four bright "candy accent" colors (emerald, steel-blue, golden-yellow, racing-red) supply the personality, and the typographic hierarchy is engineered for dashboards and spec sheets, not storefronts.

---

## Sources Used

- **`uploads/design-tokens.css`** — provided color, type, spacing, and radius tokens. This is the canonical foundation; everything in `colors_and_type.css` is derived from it.
- **Brand description (provided in chat):** "CandyCo. Full scale confectionary manufacturing partner to the largest Retail Stores in America. We private label products for Costco, Sam's Club, Trader Joes, Kroger, Walmart, Albertsons."
- _No codebase, Figma, or product screenshots were provided._ The UI kit is a faithful interpretation of the supplied tokens applied to the company's stated business — a B2B manufacturing partner site. Marked clearly so future iteration can replace assumptions with actuals.

---

## Index

```
README.md                  ← you are here
SKILL.md                   ← agent skill manifest (Claude Code compatible)
colors_and_type.css        ← canonical tokens + semantic CSS variables
assets/                    ← logos, marks, illustrations, imagery
preview/                   ← cards rendered in the Design System tab
report-template/           ← default 8.5×11 paged layout for HTML reports
complaint-response-template/ ← consumer complaint investigation response (FSQA → retail customers)
ui_kits/
  marketing-site/          ← B2B marketing site recreation (homepage + capabilities)
fonts/                     ← (Google-Fonts hosted; no local TTFs)
```

---

## CONTENT FUNDAMENTALS

**Voice — confident, plainspoken, slightly industrial.** CandyCo is the partner behind the brands you already buy. Copy should sound like an experienced ops lead, not a candy mascot.

**Casing.** Sentence case for headings and buttons. Title Case is reserved for proper nouns (product lines, retailer names) and for legal/spec callouts. ALL-CAPS is used **only** for eyebrows and tag-style labels — small, tracked-out (`letter-spacing: 0.14em`).

**Person.** "We" for CandyCo, "you" for the customer (the retail buyer / merchandiser). Never "I". Never "the user".

**Tone examples**
- ✅ "Twelve plants. One partner. Every aisle." _(headline — confident, structural)_
- ✅ "Lead times locked. Capacity allocated for Q3." _(dashboard copy — declarative)_
- ✅ "Tell us your forecast — we'll spec the line." _(CTA — collaborative, not pleading)_
- ❌ "Sweeten your shelves with our magical confections!" _(too consumer, too cute)_
- ❌ "🍬 Yummy candy for everyone! 🍭" _(emoji, exclamation, vibes only)_

**Numbers.** Always concrete. "12 plants," "1.4B units/yr," "98.7% on-time." Never "lots of" or "many." Use thin space or comma separators consistently. Percentages get the `%` symbol attached (no space).

**Plant names.** Refer to the three Lindon plants using one of these forms only:
- L1 — "L1 Caramel Plant" · "Lindon 1" · "L1"
- L2 — "L2 Moulding Plant" · "Lindon 2" · "L2"
- L3 — "L3 Chocolate Plant" · "Lindon 3" · "L3"

Do not use "Eco" / "Eco Moulding" for L2 — it is retired.

**Emoji.** Not used. CandyCo speaks to procurement teams; emoji read as unserious. Status communicated through semantic color and named tokens (success/warning/error) and short text labels ("On track," "At capacity").

**Punctuation.** Em-dashes for emphasis are welcome. Oxford comma always. No exclamation points outside of error states or genuine celebration (a successful audit, a contract win).

**Vibe.** Imagine a 1960s candy-line spec sheet redrawn for 2026 — precise, grounded, with just enough sweetness in the accent palette to remind you what business we're in.

---

## VISUAL FOUNDATIONS

**Color philosophy.** The system runs on a 10-step **Shadow Grey** scale (`#F2F2F4` → `#1A1C27`) for everything structural — text, surfaces, borders, dividers, primary buttons. Accent color is rationed: a single accent per screen, used to draw the eye to the one thing that matters (the active capacity bar, the urgent alert, the primary CTA). The "Four Candies" — emerald, steel-blue, golden-yellow, racing-red — also serve as the **utilization scale** (ramping → growing → approaching → full), which is the system's signature data-viz move.

**Typography.** Four families, three roles:
- **Yeseva One** (display) — high-contrast didone-flavored serif. Reserved for marketing display headlines, hero numbers, and section openers. The brand's most recognizable typographic move.
- **Frank Ruhl Libre** (editorial serif) — pull quotes, testimonials, long-form storytelling. Provides warmth and editorial weight where Yeseva would be too loud.
- **Assistant** (sans, 6 weights) — 90% of all UI text: body, navigation, forms, dashboards, tabular data. Activated with `font-variant-numeric: tabular-nums` for column alignment.
- **Minion Pro** (legacy serif) — held in reserve for legal, archival, and long-form documents only. Not used in product UI.

Hierarchy is established with **weight and size**, not color. Body copy is `--fg-1` (near-black); secondary text is `--fg-2`; never use accent colors as text color outside of inline status pills.

**Spacing.** Strict 4px base unit. Component-internal padding lives in the `xs/sm/md/lg` range; section-level rhythm uses `xl/2xl/3xl/4xl`. Avoid arbitrary pixel values.

**Backgrounds.** Mostly white (`--bg-1`) and pale grey (`--bg-2`). Hero sections occasionally invert to **`--primary` Shadow Grey** with white text for emphasis — this inversion is the brand's most recognizable layout move. **No gradients. No textures. No background imagery behind text.** When imagery is used (factory floors, candy production lines, finished retail-shelf shots), it is **full-bleed and uncropped**, sitting in its own band of the page rather than layered behind copy.

**Imagery direction.** Cool-leaning, daylight-color photography. Slight desaturation. Real factory floors and real production lines — never staged, never AI-rendered. Product shots are top-down on a neutral grey or deep Shadow Grey background to match the primary token. **No grain filters, no duotones, no hand-drawn illustration.**

**Animation.** Restrained. Default easing is `cubic-bezier(0.2, 0, 0, 1)` (standard) at `200ms`. Hover and press transitions only — no decorative motion, no scroll-tied parallax. The one allowed flourish is a **utilization bar fill** that animates from 0 to its target value on first paint, easing-out over 600ms.

**Hover states.** Buttons darken by one step (e.g. `--primary` → `--primary-dark`). Cards rise by one shadow level (`--shadow-sm` → `--shadow`). Links shift from `--steel-blue` to `--primary`. No scale transforms on hover.

**Press states.** Buttons shift to `--primary-dark` and shrink imperceptibly (`scale(0.98)`). Cards drop their elevation entirely (`--shadow-xs`).

**Borders.** 1px hairlines in `--border-subtle` for divisions inside cards, `--border-default` for card edges, `--border-strong` only when a control needs explicit definition (form inputs at rest). No 2px borders. No colored borders except for active/focus states.

**Shadows.** Six-step elevation system, all derived from a tinted Shadow Grey at low alpha — never pure black. Cards use `--shadow-sm` at rest; menus and dropdowns use `--shadow-lg`; modals use `--shadow-xl`. Inset shadows (`--shadow-inset`) only inside form inputs.

**Focus.** Universal `--shadow-focus` ring — `0 0 0 3px rgba(25, 130, 196, 0.25)` — the steel-blue accent at 25% alpha. Visible on every interactive element, no exceptions.

**Capsules vs. protection gradients.** Status and category labels are **capsules** (pill-shaped, `--radius-pill`) with a tinted background (`--success-bg`, `--warning-bg`, etc.) and the matching strong color as text. Protection gradients (dark→transparent overlays on imagery) are not part of this system — text always lives outside imagery, never on top of it.

**Layout rules.** 12-column grid at `1280px` content width. Header is fixed (sticky) at the top, 64px tall. No sidebars on marketing pages; sidebars appear in the (forthcoming) operator dashboard product. Footer is full-width on `--primary`.

**Transparency & blur.** Used in exactly one place: the sticky header has a `rgba(255,255,255,0.85)` background with `backdrop-filter: blur(12px)` once the user scrolls past 8px. Otherwise opacity is binary — fully visible or hidden.

**Corner radii.** Default `--radius` (10px) for buttons and cards. Inputs use `--radius-sm` (6px). Modals and feature panels use `--radius-xl` (20px). Capsules use `--radius-pill`. **Never zero radius** except on data-table cells.

**Cards.** White background, `--border-subtle` 1px hairline, `--radius` corners, `--shadow-sm` at rest, `--shadow` on hover. Internal padding `--spacing-lg` (24px). **No accent stripes — top, left, or otherwise.** A tropey pattern we explicitly avoid. When a slide or screen shows multiple cards side-by-side, every card is the same neutral object; meaning lives in the data inside, never in a colored border. Presentation-context cards (slide decks) skip the hairline border and lean harder on shadow — see PRESENTATIONS & SLIDE DECKS below.

---

## ICONOGRAPHY

**System: Lucide Icons (CDN-linked).** No proprietary icon set was provided. We standardize on [Lucide](https://lucide.dev) — a 1.5px-stroke, rounded-corner, line-weight-consistent set that pairs cleanly with IBM Plex's geometric humanism. Loaded from CDN; see `assets/icons/README.md`.

**Stroke weight.** 1.5px default; 2px only for icons rendered ≤16px where 1.5 antialiases poorly.

**Icon size scale.** 16 / 20 / 24 / 32 / 48px. 20px is the default in-line size; 24px in primary navigation.

**Icon color.** Inherits from text color (`currentColor`). Never colored independently. Status icons (✓ success, ! warning) take their semantic color from the surrounding capsule, not from the icon itself.

**SVG vs. font.** SVG only. No icon fonts. Each icon is a single `<svg>` element inline.

**Emoji.** **Not used in product UI** — see Content Fundamentals. Permitted in internal Slack and external social copy, never in shipping interfaces.

**Unicode glyphs.** Permitted for typographic punctuation only (em-dash, en-dash, curly quotes, ×, →, ←, ↑, ↓). Not as decorative icons.

**Logo.** The CandyCo logo is a candy-wrapper mark above a custom wordmark. Three files live in `assets/logo/`:
- `candyco-logo-black.png` — primary, on light surfaces.
- `candyco-logo-white.png` — reverse, on `--primary` Shadow Grey.
- `candyco-mark.jpg` — the wordless wrapper mark for tight spaces and avatars.

**Substitution flag.** Lucide is a substitution. If CandyCo has a proprietary icon set, please share it and we'll swap.

---

## REPORTS & PAGED DOCUMENTS

**Every CandyCo HTML report defaults to the paged 8.5×11 layout in
`report-template/`.** Reports, briefings, analyses, recaps, dashboards
distributed as documents, and any long-form HTML belong in this format unless
the user explicitly asks for something else.

The format is non-negotiable on three points:

1. **Discrete sheets, not continuous flow.** Each section lives inside a
   `<section class="sheet">` that renders as an 8.5" × 11" white page on
   screen and prints as one page on Letter paper. The reader sees the page
   boundaries while drafting and gets a clean PDF on print.
2. **Logo lockup in every cover header.** The official `candyco-logo-black.png`
   sits at 42px height beside the document meta (eyebrow + date + scope).
   Both logo PNGs carry a 4% transparent margin so no artwork sits on the
   image boundary — the 42px box renders the artwork at the standard 38px.
   Never substitute with a text wordmark. Use the white logo on inverse
   Shadow Grey blocks.
3. **Page-numbered footers on every sheet.** `[Doc title] · Page N of M` in
   the bottom strip. Footer-derived page numbers are part of the trust signal —
   the reader knows the document is intentional, not a print accident.

To start a new report, copy `report-template/template.html` and follow the
instructions in `report-template/README.md`. The component library —
hero callout, stat strip, capsules, audience grid, action-assignment table,
chart card, footnote — is already wired up and uses only tokens from
`colors_and_type.css`.

**Consumer complaint investigation responses** (the quality team's written
response to a retail or brand customer) start from
`complaint-response-template/template.html` instead — a pre-structured
4-page customer report plus two internal guidance pages (timelines, severity
classification, writing rules, pre-send checklist). See
`complaint-response-template/README.md`.

**Skip the paged layout only when** the user says "raw," "single page,"
"one-pager," "no branding," "quick draft," "dashboard," "slide," or asks for
a non-paged format outright.

---

## PRESENTATIONS & SLIDE DECKS

**Every CandyCo board deck defaults to the *Board Deck Style*** — a 16:9 canvas with a two-theme split, white cards lifted on a cool-grey body, no top-edge accent stripes, and copper reserved for the dark-slide editorial chrome only.

The canonical reference + reusable stylesheet + starter template live in **`board-deck/`** — see `board-deck/README.md` for full details. New decks copy `board-deck/template.html` and `@import` `board-deck/board-deck-style.css`; do not rebuild the pattern from scratch.

### Canvas

- **Light content slides** (`data-section="financial" | "operations" | "sales" | "capacity" | "fsqa" | "customer" | "plant"`): cool-grey `#F2F2F4` canvas, white cards lifted via soft shadow, **white title bar at top + white footer bar at bottom**, dark navy type, no copper text anywhere. Letterboxed by the deep Shadow Grey body background when the viewport isn't exactly 16:9.
- **Dark slides** (cover, agenda, dividers, closing): `--shadow-grey-900` page, ivory type, copper accents. A ghost `candyco-logo-white.png` wordmark sits in the bottom-right at ~6% opacity — felt, not read. Don't add a ghost watermark to light slides; the visual tried it and felt heavy.

### Title + footer bars (light slides only)

The Board Deck Style locks the slide chrome into two horizontal white bars at the top and bottom of every light slide:

- **Title bar (top, white, full slide width):** CandyCo wordmark logo + "Board Deck · `<date>`" deck-identifier eyebrow on the left, section info (e.g., "I · Financial update") on the right. The slide title (`<h2 class="slide-title">`) flows directly below as part of the same white bar — separated from the body canvas by a 1px hairline.
- **Footer bar (bottom, white, full slide width):** "Confidential · Internal use only" on the left, page number on the right. No logo, no center wordmark.

The original copper slide-eyebrow + copper slide-rule are hidden on light slides — the bar's bottom hairline replaces the rule, and the section anchor in the title bar replaces the eyebrow.

### Card panels — the deck rule that supersedes everything else

KPI tiles, data tables, op-metric callouts, partner stats, and every other panel that sits on a light slide all share one treatment:

- **White (`#FFFFFF`) background, no exceptions.** Don't tint cards ivory, sand, cream, or any warm neutral — they read as tan against the white canvas. The earlier ivory `#F5F2EC` panel fill is retired in favor of white.
- **14px corner radius** — softer than the standard `--radius` UI 8px; reads as paper-resting-on-paper at presentation distance.
- **Soft two-layer shadow, no hairline border.** Board Deck Style shadow recipe:
  ```css
  box-shadow:
    0 1px 3px  rgba(26, 28, 39, 0.06),
    0 12px 32px rgba(26, 28, 39, 0.08);
  ```
  This lands between `--shadow` and `--shadow-lg` — more lift than a UI card, less than a modal — and is the right weight for cards floating on a cool-grey slide canvas at presentation distance.
- **No accent stripes — top, left, or otherwise.** Same rule as `Cards` above, restated because the deck context is where this rule matters most. Eight panels on a slide with four different colored top stripes (blue / gold / green / copper) reads as decoration, not meaning. Strip them.
- **Tighter padding than UI cards** (~12–16px instead of 24px). Decks reward density; readers absorb whole slides at a glance, not card-by-card.

### Status dots + yellow tag chips

Two quiet signal patterns earn their place in the Board Deck Style:

- `<span class="dot fav|unfav|neutral">` — a 7×7px leading dot on KPI labels, op-metric labels, and notable customer rows. Emerald = favorable, racing-red = unfavorable, grey = neutral. The one quiet color signal that replaces the abandoned colored top-stripes.
- `<span class="tag-chip">P&L</span>` — golden-yellow categorical chip used at most once per panel eyebrow to label what the card is (mirrors the "SHARED" tag pattern in the org chart). Never as decoration.

### Color in charts and KPIs

Color carries meaning, not category.

- **Emerald** — favorable, better than budget, above goal.
- **Racing red** — unfavorable, worse than budget, below goal.
- **Neutral grey** — at-target, informational, "no signal."
- **Steel-blue** — baseline / "budget" / committed plan, used as the left half of a budget-vs-forecast bar pair.
- **Golden-yellow** — warning, approaching threshold, "still in pipeline" (e.g., Pistachio-style pipeline bars).
- **Copper** — editorial chrome only (slide eyebrow, slide-rule, active nav-dot, dashed budget-goal reference line). Never inside a card.

**Do NOT assign blue / gold / green / copper as the visual identity of individual KPI tiles.** Every tile is the same white neutral object. The Net Revenue tile and the Gross Margin tile look identical — meaning is communicated by the data inside (chip color, delta sign, py-line direction), not by chrome.

### Chart cards — lock aspect, lose the letterbox

When an SVG chart card has a fixed `viewBox` (e.g. `0 0 620 410`), give the **card itself** the matching `aspect-ratio`. Otherwise the card stretches to the row height, the chart's `preserveAspectRatio="xMidYMid meet"` scales by width, and dead space appears as top + bottom letterbox inside the card.

```css
.chart-card {
  aspect-ratio: 620 / 410;   /* matches the SVG viewBox */
  align-self: center;        /* balance leftover row space top/bottom */
}
```

`align-self: center` (not `start`) keeps the cards visually anchored in the row instead of pinned to the top — the leftover slide-level space splits evenly above and below, which reads as breathing room rather than abandonment.

### Paired bars — when one period needs two values

Some periods carry two related values (e.g., 2026 Budget vs Forecast). Render both as **full-width** bars, not half-width — the period should read with the same visual weight as every other:

- **Each bar in the pair: same width as a single-year bar** (e.g., 36px in a 60-spaced grid).
- **2px gap between the pair members** — keeps Budget and Forecast tightly grouped as one period.
- **Standard year-to-year gap separating the pair from the previous year** — same as every other transition (e.g., 24px in a 60-spaced grid). Without this gap, 2025 and 2026 read as one fused blob.
- **Steel-blue for the Budget half, emerald for the Actual/Forecast half** — see Color in charts and KPIs.

This is the one chart pattern where steel-blue and emerald appear next to each other inside a single chart, and they carry semantic weight (budget vs. forecast). Don't reuse this exact color pair for unrelated categorical groupings.

### PowerPoint translation

PowerPoint decks follow the same content rules as HTML decks. The translation:

- **Slide backgrounds:** white for content sections, `--shadow-grey-900` for cover + dividers. Set as theme background colors so every new slide inherits.
- **Cards** are PPT rectangles with **white fill, no outline, ~8px rounded corners, soft Outer Shadow** (PowerPoint preset → Outer → "Offset: Center" or similar, kept at low intensity). Avoid the harder "Offset Bottom" preset; it reads more UI than paper.
- **No top-border accent stripes** on shape callouts — same rule as HTML.
- **Theme colors** in PPT are pinned to the CandyCo palette (Shadow Grey 50–900, Emerald, Racing Red, Steel-blue, Golden-yellow, Copper). Never paste hex values into individual shapes; if you have to override, the theme is wrong.
- **Charts** are inserted as native PowerPoint chart objects (not pasted images). Their color scheme is bound to the theme so a single recolor on the theme cascades to every chart.
- **Type** uses the embedded Yeseva One (display), Frank Ruhl Libre (editorial), and Assistant (body) families. If the recipient doesn't have these installed, PPT must embed the fonts on save (File → Options → Save → Embed fonts in the file).

---

## CAVEATS & FONT SUBSTITUTIONS

- **Fonts:** Real brand fonts are loaded locally from `fonts/` — **Assistant** (sans), **Frank Ruhl Libre** (serif), **Yeseva One** (display), **Minion Pro** (legacy). The `--font-family` token in the original tokens file (system stack) has been superseded by `--font-sans` etc.
- **Imagery:** No photography assets were supplied. Marketing site uses CSS-only placeholder bands where photography would live in production.
- **Product surfaces:** Only a marketing-site UI kit is included. If CandyCo has an operator dashboard, retailer portal, or QC app, please share screenshots or codebase access.
