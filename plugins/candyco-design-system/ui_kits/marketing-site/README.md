# Marketing Site — UI Kit

A faithful interpretation of CandyCo's B2B marketing surface, derived from the design tokens. No source codebase or Figma was provided — components here are recreations sized to plug into the design system, not screenshots of a real site.

## Components

- **`Header.jsx`** — sticky top nav with logo, links, sign-in, primary CTA. Backdrop-blurs on scroll.
- **`Hero.jsx`** — full-bleed Shadow Grey hero with display serif headline + dual CTAs.
- **`StatStrip.jsx`** — four-up KPI numbers in display serif (12 plants / 1.4B units / 98.7% on-time / 6 retailers).
- **`CapabilityCard.jsx`** — feature card with Lucide icon, title, body copy.
- **`UtilizationPanel.jsx`** — signature data-viz: live plant capacity bars using the four-color utilization scale.
- **`RetailerStrip.jsx`** — pill row of retail partner names.
- **`Footer.jsx`** — full-width Shadow Grey footer with wordmark, link columns, legal.

## Notes

- All components consume tokens from `../../colors_and_type.css` only — no hardcoded colors.
- Lucide icons are loaded via CDN.
- This is a **marketing surface only**. If CandyCo has an operator dashboard, retailer portal, or QC app, those are separate kits to be added.
