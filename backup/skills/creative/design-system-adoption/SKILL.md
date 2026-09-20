---
name: design-system-adoption
description: "Use when adopting an external design system into a web app."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [UI, UX, Design Tokens, CSS, Web Development, Redesign]
---

# Design System Adoption into Web Frontends

Adopt design patterns from an external design system / UI kit / skill repo (e.g. shadcn-style tokens, Tailwind-like scales, a GitHub reference repo) into an existing web project — especially restyling a working vanilla HTML/CSS/JS app without breaking its behavior. Also covers polished theming (dark/light), accessibility passes, and verifying the result in a real browser.

## Core principle: restyle, never rebuild logic

A UI redesign on a working app has ONE hard requirement: every behavior keeps working. Before touching any CSS/HTML, extract the **functional contract**:

```bash
grep -oE 'getElementById\([^)]+\)|querySelector[^;]+|function [a-zA-Z]+' index.html | sort -u
```

List every element ID, class hook, and global function name the JS references. The redesigned markup MUST expose the same IDs and the script MUST keep the same function names/signatures. Rename nothing.

## Workflow

1. **Fetch the reference source** (shallow clone to /tmp, never into the project):
   ```bash
   rm -rf /tmp/<ref-name> && git clone --depth 1 <repo-url> /tmp/<ref-name>
   ```
   Read its SKILL.md / references / templates first — most design repos document their own token architecture.

2. **Inventory what to adopt** in three buckets: design tokens (colors/type/spacing/radius/shadow/durations), component patterns (buttons/cards/badges/inputs + their variant matrices), and example projects (real usage: navbars, heroes, glows, glass effects).

3. **Map tokens as a 3-layer CSS architecture** (see `references/` for a filled-in bank and `templates/tokens-root.css` for a starter):
   - Primitive: raw scales (`--slate-*`, spacing on a 4px base `--space-N`, `--text-xs…5xl`, radius, shadow, duration fast/normal/slow).
   - Semantic: intent names mapped onto primitives (`--background`, `--foreground`, `--primary`, `--muted-foreground`, `--border`, `--ring`). Define BOTH themes here: default theme in `:root`, override in `[data-theme="light"]`.
   - Component: per-component knobs consuming semantics (`--btn-padding-x: var(--space-4)`).

4. **Restyle** using the contract from above:
   - Component classes with shadcn-style variants (`.btn-default|outline|ghost|secondary|destructive|icon`, `.badge-*`, `.alert-*`) + a thin Tailwind-like utility layer (only the utilities you actually use).
   - Interactivity polish: hover lift + glow shadow, active press `scale(0.97)`, animated icon swaps, value-change pulse micro-interactions.
   - Accessibility: skip-link, single `:focus-visible` ring token (`0 0 0 2px var(--background), 0 0 0 4px var(--ring)`), `aria-expanded` on disclosure cards, `aria-live="polite"` on result regions, real `<button>`s instead of clickable divs, `<label for>` on sliders.
   - Theming: `data-theme` attr + `color-scheme` meta; JS init reads localStorage → falls back to `prefers-color-scheme`; persist toggles in try/catch (private mode throws).
   - Motion: CSS `@media (prefers-reduced-motion: reduce)` zeroing durations AND a `matchMedia('(prefers-reduced-motion: reduce)')` guard around JS animation loops (setInterval animations, smooth scroll).
   - Responsive: mobile-first grid with explicit breakpoints (e.g. 640/1024/1440px) and stacked layouts under 640px.

5. **Verify in a real browser** (see Pitfalls for why console-eval beats ref-clicking):
   ```bash
   # background=true, NOT shell '&'
   cd <project> && python3 -m http.server <port> --bind 127.0.0.1
   ```
   - `browser_navigate` → confirm interactive elements exist.
   - Functional asserts via `browser_console` with an IIFE: set slider `.value`, `dispatchEvent(new Event('input'))`, then READ the computed outputs (ratio text, hex, totals) and return JSON.
   - Call the theme toggle function, assert `document.documentElement.getAttribute('data-theme')` flips.
   - Vision screenshot BOTH themes; check contrast, badges, gradients, layout glitches.

6. **Commit** with a message describing WHICH patterns were adopted (token layers, component variants, a11y additions) — reviewers should see the design provenance, not just "update styles".

## Pitfalls

- **Renaming IDs/functions during restyling = silent breakage.** The page renders fine and every interaction is dead. Always grep the contract first.
- Inline `onclick="fn()"` handlers often rely on the implicit global `event` object — fragile under `'use strict'`. Prefer event delegation: `addEventListener` + `data-*` attributes, keep `fn()` callable for compatibility.
- Browser element ref IDs (@eN) go STALE across vision/snapshot/navigation round-trips → clicks fail with "Unknown ref". Re-snapshot, or better: drive state changes and assertions through `browser_console` JS evaluation and reserve clicks for simple entry points.
- Range inputs need per-engine styling (`::-webkit-slider-thumb` AND `::-moz-range-thumb/progress`). For a filled track, paint a `--fill` percentage custom property from JS (`paintSlider`) and use it in the webkit track gradient; Firefox has native `::-moz-range-progress`.
- Dark-by-default pages: don't hardcode dark in `:root` alone — JS must resolve localStorage/system preference on load or light-mode users get flashed the wrong theme.
- `prefers-reduced-motion` in CSS does NOT stop JS `setInterval` position updates — gate those separately or the "static" page keeps burning CPU.
- When a panel/card opens, scroll it into view respecting reduced motion (`behavior: reducedMotion.matches ? 'auto' : 'smooth'`).

## Reference files

- `references/ui-ux-pro-max-tokens.md` — condensed token bank + component/example-project patterns extracted from nextlevelbuilder/ui-ux-pro-max-skill (reusable as an authoritative baseline).
- `templates/tokens-root.css` — copy-paste starter: full primitive + semantic + component token `:root`/`[data-theme="light"]` block proven in production.
