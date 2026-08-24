# SVG Showcase

Twelve examples demonstrating two Hermes skills:

- **svg-skill** — production-ready static SVG markup (icons, charts, flowcharts, logos, avatars)
- **visualise** — inline interactive visuals (comparisons, metric cards, explainers, Chart.js charts, architecture diagrams, data records)

## View

Open [`index.html`](index.html) — it embeds all six SVGs and links to all six interactive widgets.
On GitHub Pages every asset resolves relatively; each `examples/*.html` page is also fully self-contained.

## Structure

```
svg-showcase/
├── index.html              # Responsive showcase grid
├── examples/
│   ├── icons.svg           # 6 outline UI icons (24×24 grid, scaled sheet)
│   ├── progress-rings.svg  # 4 progress rings via stroke-dasharray (25/50/75/100%)
│   ├── bar-chart.svg       # Horizontal bar chart, title+desc, axis ticks
│   ├── flowchart.svg       # 5-step process flow with marker arrows
│   ├── logo.svg            # HERMES brand mark + wordmark lockup
│   ├── avatars.svg         # 4 initials avatar placeholders (ZH MX EL CH)
│   ├── comparison.html     # Side-by-side agent comparison cards
│   ├── metrics.html        # 4 KPI metric cards grid
│   ├── explainer.html      # Interactive slider → live model output
│   ├── pie-chart.html      # Chart.js donut (token spend by phase)
│   ├── architecture.html   # Structural system diagram (SVG, 680 viewBox)
│   └── data-table.html     # Styled data record card
└── README.md
```

## Design system — MyStyle1

| Token | Value |
|-------|-------|
| Font | Inter (Google Fonts), weights 400/500/600 |
| Ink | `#0f172a` |
| Accent | `#f97316` |
| Paper | `#ffffff` |
| Background | `#f8fafc` |

Rules applied throughout: **flat fills only** (no gradients/shadows), max 2–3 color
families per diagram, visualise diagrams use a **680px-wide viewBox**, labels 14px,
subtitles 12px, minimum 11px.

## Accessibility

Every SVG carries `xmlns`, a `viewBox`, and either `role="img"` +
`aria-labelledby` pointing at `<title>`/`<desc>` (informative graphics) or
`aria-hidden="true"` (decorative marks). Charts summarize their data in `<desc>`.

## Validation

```bash
# SVG quality gates (xmlns, viewBox, placeholders, editor metadata, XML well-formedness)
bash /opt/data/skills/svg-skill/scripts/validate.sh examples/

# Inline JS syntax check (extracted from each HTML file)
node --check <extracted-script.js>
```

## Regenerating

SVGs are hand-authored source — edit them directly; coordinates for the bar chart
follow `x = 178 + pct × 4`, ring dasharrays follow `2πr ≈ 188.5` at `r = 30`.
