---
name: web-slide-decks
description: Use when asked to build a single-file HTML slide deck.
version: 1.5.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [web, presentation, slides, html, frontend]
---

# Web Slide Decks (Single-File HTML)

Use when the task is "buatkan presentasi / slide deck / web presentation" and the
deliverable is ONE self-contained `.html` file: no external libraries, emoji icons,
system fonts, light modern theme (Apple/Google design language). Proven end-to-end
on a 19-slide AI presentation (`labsdigital/hermes` → `elon/presentasi-ai.html`) and
a 29-slide math presentation (`elon/rasio-perbandingan-lengkap.html`) and its full
Modern Professional restyle (`elon/rasio-perbandingan-v2.html`), and the
scrollable-slides evolution through `elon/rasio-perbandingan-v5.html`
(41 slides, 10 labs, active-slide scrolling), and the desktop-application
shell variant `elon/rangkaian-listrik-v2/index.html` (EduApp2, 2026-08-24:
fixed collapsible sidebar + topbar instead of a floating dock — see
"Chrome" and `references/desktop-app-shell-eduapp2.md`).

## Core Architecture (do it this way)

- Each slide = `<section class="slide">`, absolutely positioned `inset:0`,
  `overflow:hidden` by default (keeps transitions clipped). Toggle an `.active`
  class — NEVER `display:none` (kills smooth transitions). For decks with
  labs/quizzes/reveals, make the ACTIVE slide the scroll container — see
  "Scrollable Active Slides (v5 pattern)" below.
- Slide transition: default `opacity:0; visibility:hidden;
  transform:translateY(26px) scale(.99)` with a delayed `visibility` transition;
  `.active` fades/slides in with ~60ms delay so exit starts first.
- Inner wrapper centers content AND allows scrolling when tall:
  `.inner{max-width:1120px;margin:0 auto;min-height:100%;display:flex;
  flex-direction:column;padding:86px 28px 106px}`
  (bottom padding clears the fixed nav bar). Center with AUTO margins
  (`.inner>*:first-child{margin-top:auto}`, `.inner>*:last-child{margin-bottom:auto}`) —
  `justify-content:center` clips the top of overflowing scrollable content (see Pitfalls).
- Staggered content reveal: `.reveal{opacity:0}` +
  `.slide.active .reveal{animation:rise .6s cubic-bezier(.22,.61,.36,1) forwards;
  animation-delay:var(--d,0s)}`, each element gets inline `style="--d:.16s"`.
  Removing `.active` resets it for re-entry.
- Per-slide accent theming: every section carries
  `style="--accent:#hex" data-accent="#hex" data-label="Bab 1 · …"`.
  All descendant styling reads `var(--accent)`; JS recolors the chrome
  (progress bar, chapter chip) from `data-accent`. UNIFIED-ACCENT VARIANT
  (Modern Professional rebrands): drop per-chapter hues entirely — one accent
  for the whole deck, attrs stripped by regex, `paint()` reduced to bar-width +
  counter + chip label. See "Restyling an Existing Deck".

## Scrollable Active Slides (v5 pattern — dense/interactive decks)

Validated on `elon/rasio-perbandingan-v5.html`. Briefs with labs/quizzes/
steppers/reveals WILL overflow on short viewports; plain `overflow:hidden`
silently clips them (the v1–v4 defect this pattern fixes).

- CSS: keep `.slide{overflow:hidden}` for transitions; add
  `.slide.active{overflow-y:auto!important;overflow-x:hidden;overscroll-behavior:contain;
  scroll-behavior:smooth}` + thin accent scrollbar. `.inner` keeps min-height:100%
  flex with AUTO-margin centering; bottom padding (~132px) clears the fixed dock.
- needs-scroll detection MUST compare `.inner.offsetHeight > slide.clientHeight+2`.
  NEVER `slide.scrollHeight` — absolutely-positioned decorations (cover dotgrid
  `top:-40px;height:120%`, divider ghostnum `bottom:-90px`) inflate it and flag
  slides whose content actually fits (shipped bug, caught in render test).
- Scroll hint: inject one pill per slide via JS (not per-slide markup); show only
  when `.needs-scroll`, fade at bottom via passive scroll listener toggling
  `.scrolled-end`. Slides get `tabindex="-1"` + `focus({preventScroll:true})` in go().
- Keyboard: Space/PageUp/PageDown/ArrowUp/ArrowDown scroll the slide FIRST
  (~82% viewport step), navigate only at edges; Left/Right always change slides.
  `go()` resets `slides[cur].scrollTop=0` (slide is the scroller now).
- Reveals: after toggling answer boxes/quiz feedback, re-run detection and
  `scrollIntoView({behavior:'smooth',block:'nearest'})` after ~120ms. Any
  `max-height` reveal is a clip risk — budget generously (`.ansbox.on` needed
  420px → 1100px). Print: `.slide{overflow:visible!important}`, hide hints.
- Full CSS/JS snippets, keyboard map and render-test matrix:
  `references/scrollable-slides-v5.md`.

## Chrome (fixed UI)

- Top: 4px progress bar, width = `(current+1)/total %`.
- Top HUD: two white pills — chapter label (left, tinted with accent),
  counter `n / total` (right).
- Bottom nav bar centered: round prev/next buttons + dot strip. Dots as pills:
  inactive 8px circle, `.active` stretches to 22px wide with accent fill.
  Disable prev on first slide, next on last.
- Background: 2–3 large blurred gradient blobs (position:fixed,
  filter:blur(90px), low opacity) behind everything for depth while staying light.
- Spec variant (no-dots chrome): some briefs demand NO dots/bullets with
  prev/next at bottom-RIGHT (shipped: `elon/rasio-perbandingan.html`). Keep
  go()/paint(), hash and swipe identical; drop the dots markup + logic, position
  the bar with `.nav-bar{right:22px;bottom:22px}` (no centering transform), and keep
  the keyboard target-guard from Navigation JS — such decks carry sliders.
- Desktop-app shell variant (EduApp2): chrome becomes a fixed 56px topbar
  (hamburger, uppercase title + version badge, N/17 counter, icon buttons,
  3px progress bar on its bottom edge) plus a fixed 260px dark-slate sidebar
  listing ALL slides 1:1 (`<button data-i="N">`: number/chapter badge + title +
  muted subtitle; dividers B1–B5, labs L1–L3). Content is a fixed pane
  (`left:260px`, dot-grid texture) holding white "tech frame" cards with an
  orange top accent and a per-slide header strip (kicker left, `N / 17`
  right); pager stays bottom-right, no dots. Collapse: desktop animates
  sidebar `width:260px→0` + content `left→0` (.3s, inner column keeps fixed
  min-width); ≤900px switches to a translateX overlay + dimmed backdrop,
  branched via `matchMedia` body classes with a `change` listener that strips
  the other mode's class; Escape/backdrop close on mobile. `paint()` syncs the
  sidebar (`.on` + `aria-current` + `scrollIntoView({block:'nearest'})`).
  Small type scale (body 14–16px, headings 22–26px) — this is an APP look,
  not projection. Full validated pattern + test recipe:
  `references/desktop-app-shell-eduapp2.md`.

## Modern Split-Pane Desktop Pattern (taraka.id style)

When the brief references `https://taraka.id/AGENTS/ui.txt` or asks for a
"desktop app" aesthetic, use the Modern Split-Pane Desktop pattern:

- **Layout**: Left sidebar (300px, dark #09090b) + Main workspace (light #fafafa)
- **Sidebar**: Accordion navigation with group headers, active state with orange left border
- **Workspace**: Window header (56px) with controls, scrollable content area
- **Cards**: `.desktop-card` with rounded-3xl (24px), border #e4e4e7, shadow
- **Typography**: Inter font, 2-Tone Headings (black + orange accent)
- **Navigation**: FAB buttons (Home, Prev, Next) at bottom-right, 56px circular
- **Reference**: See `references/modern-split-pane-desktop.md` for full spec

Example: `elon/computational-thinking/index.html` (2026-08-24)

## Navigation JS (~50 lines, one IIFE)

- `go(n)` clamps to range; skips work if index unchanged; scrolls activated
  slide back to top.
- Keyboard: ArrowRight/PageDown/Space → next, ArrowLeft/PageUp → prev,
  Home/End; bail out when ctrl/meta/alt held; preventDefault on handled keys.
  Interactive decks: bail per target type. INPUT/TEXTAREA/SELECT → bail from
  ALL deck keys (a focused range slider must own ←/→). BUTTON → bail ONLY the
  scroll/activate keys (Space/PageUp/PageDown/ArrowUp/ArrowDown) but KEEP
  ArrowLeft/Right/Home/End global — app-shell decks are full of focusable
  sidebar/pager buttons, and a full BUTTON bail makes ←/→ dead right after any
  button click. Proven in `elon/rasio-perbandingan.html` and
  `elon/rangkaian-listrik-v2/index.html`.
- Touch swipe: record touchstart X/Y, on touchend fire if |dx|>56 and |dx|>|dy|.
- Deep links: on load parse `location.hash` → open that slide; on every change
  `history.replaceState(null,'','#'+n)`. So `deck.html#7` opens slide 7.
- Jump targets: any element with `data-goto="n"` gets a click listener — use for
  clickable agenda cards (jump to chapter dividers) and a restart button.

## Responsive / A11y / Print

- Grids collapse at 960px and 700px; hide dots <700px (counter + swipe still
  navigate); horizontal pipelines become vertical columns with arrows rotated 90°.
- `@media (prefers-reduced-motion:reduce)`: kill all animation/transition,
  force `.reveal{opacity:1}`.
- `@media print`: slides become `position:relative; min-height:100vh;
  page-break-after:always`, everything visible, chrome hidden — the deck doubles
  as a PDF handout for free.

## Visuals Without Libraries

- Neural networks / graphs: inline `<svg viewBox>` — circles for nodes,
  low-opacity lines for edges, CSS keyframe pulse on output nodes.
  Set `font-family` on svg `<text>` explicitly.
- Nested concepts (AI ⊃ ML ⊃ DL): nested rounded divs, each ring a tinted bg +
  colored border.
- Step pipelines: flex row of cards separated by `➜` glyphs.
- Progress meters: `.meter > i{width:var(--w)}` where `--w` animates from 0 when
  the parent slide gets `.active` (transition-delay ~0.5s).
- Emoji favicon: `<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22…%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🤖</text></svg>">`.

## Pro Max Tier (design tokens, dark mode, glassmorphism)

When the brief asks for "UI/UX Pro Max" quality, PPT-scale typography, or a
dark/light toggle, keep the base architecture above and upgrade the styling layer:

- Define everything as `:root` tokens: projection-sized type scale via `clamp()`
  (hero ≈92px, slide title ≈60px, card h3 ≈28px, body ≈26px, caption ≈20px),
  spacing scale, radii 14/20/28px, two shadow tiers (rest + hover-lift), and named
  gradient tokens (violet→blue, orange→pink, orange→teal). Body text must land 24–32px on a
  desktop viewport for presentation use.
- Dark/light toggle = token overrides on `body.dark` (bg/text/muted/glass/shadow),
  HUD pill button, persisted in localStorage, fallback to `prefers-color-scheme`.
- Glassmorphism cards: translucent bg + border tokens +
  `backdrop-filter:blur(20px) saturate(160%)` (include `-webkit-`); reads well over
  the blurred bg blobs in both themes.
- Full-bleed cover/closing bookends: section paints its own multi-stop gradient and
  holds absolutely-positioned blurred glow divs; `.inner` needs
  `position:relative;z-index:1`. Chrome pills keep their own glass background so
  they stay legible on top.
- Ready-made token block, dark overrides, glass CSS, toggle JS and per-slide
  gradient chrome: `references/pro-max-patterns.md`.

## Restyling an Existing Deck (token-swap redesign)

When the job is a REDESIGN/rebrand of a deck whose content + interactive JS must
survive intact, do NOT hand-rewrite the whole file — transcription errors across
hundreds of JS lines are the #1 risk. Proven on
`rasio-perbandingan-lengkap.html` → `-v2.html` (83KB, 29 slides, every slider/
quiz/stepper preserved byte-for-byte):

1. Read the original fully; inventory every class, every `id="…"`, and every
   element the script touches (`$('…')`, querySelector targets).
2. Author the NEW design system as a standalone `<style>` replacement, keeping
   old class names stable wherever semantics match (`.card`, `.badge`, `.ctl`,
   `table.data`, `.tile`, …) so untouched markup just re-renders under it.
3. **Token-alias trick** — legacy tokens/classes that no longer fit get
   REDEFINED, not deleted. Markup that still says `background:var(--grad-ot)` or
   `<span class="grad">` renders correctly under the new look if the new sheet
   declares `--grad-ot:#f97316` (solid!) and `.grad{color:var(--accent)}`.
   Zero markup churn where possible.
4. Moving to ONE unified accent: strip per-slide theming via regex —
   `\s+data-accent="[^"]*"`, `\s+data-grad="[^"]*"`,
   `\s+style="--accent:[^"]*"` — and simplify `paint()` to bar-width +
   counter + chip label with a static accent progress fill.
5. **Split the document at `<script>` before any hex/color replaces.** Recolor
   the markup side freely (`#14b8a6 → var(--accent)`), but handle JS string
   literals deliberately (`'#14b8a6' → '#f97316'` for chart params) so blind
   global replaces can never corrupt code.
6. Rewrite wholesale ONLY sections whose structure actually changes (gradient
   cover/closing → clean light bookends); everything else stays untouched.
7. Stage scratch assets (new CSS block, replacement sections, the Python/regex
   stitcher) under the WORKSPACE (e.g. `/opt/data/.tmp-v2/`) — this deployment
   denies writes outside the workspace root (HERMES_WRITE_SAFE_ROOT), so `/tmp`
   is not available; delete the staging dir after assembly.

Extra verification beyond the standard suite: assert `<section` count matches,
extract the script for `node --check`, build the set of `$('id')` references from
the script and diff against `id="…"` occurrences in markup, and grep for stray
old-palette hexes (fallback colors hide inside inline styles).

## Validation Workflow (run ALL before committing)

Automated runner for the static steps: `python3 <skill_dir>/scripts/validate_deck.py
<deck.html> [--expect-slides N] [--need-ids id1,id2] [--allow-dots]` — slide
count, `node --check`, tag balance, empty placeholder artifacts, required ids,
leftover dot-nav detection.

1. Slide count matches spec: `grep -c '<section class="slide' deck.html`.
2. Extract inline `<script>` to a temp file → `node --check` it.
3. Tag balance: small Python `html.parser.HTMLParser` subclass tracking a stack
   (skip void tags + svg leaf tags) — report mismatches/unclosed.
4. Render test: `browser_navigate` to `file://…/deck.html`, confirm snapshot
   (counter, dots count, disabled prev), click next twice, screenshot.
5. Deep-link gotcha: navigating from `deck.html` to `deck.html#7` is
   SAME-DOCUMENT — Chromium doesn't reload on fragment-only changes, so the
   jump won't fire unless the deck also listens for `hashchange`. To verify
   fresh-load deep links, open `about:blank` first, then load `file://…#N`.
6. Drive one interactive widget per mechanism, not just navigation: set a
   range slider value + dispatch `input` event, click a reveal button, submit
   a wrong then a right check-answer — confirm computed text updates.

## Pitfalls

- **Scroll vs no-scroll decision**: When brief says "fit 1 layar / no scroll", use `overflow:hidden` on `.slide`. BUT when content genuinely exceeds viewport (dense labs, quiz feedback, steppers), allow `overflow-y:auto` on `.slide.active` ONLY — keep transitions clipped on non-active slides. Always add scroll-hint indicator for tall slides. See V5 pattern in `references/scrollable-slides-v5.md`.

- **Eye-catching but not distracting**: Orange-teal gradients are great for covers WHEN the brief allows gradients. Don't overdo saturation. Use `opacity:.85` or soften one stop if the gradient feels harsh on a projector. BUT some briefs explicitly BAN gradients on title/closing slides (Modern Professional / Apple-like specs): then ship pure-white bookends instead — huge slate-900 display type, orange tagline line, bordered stat chips, and a masked dot-grid corner texture for depth. Either way keep bookend text minimal (title + subtitle only, no extra prose).

- **Emoji restraint**: When brief specifies "minimal emoji" or targets SD (elementary school) audience, use MAXIMUM 1 emoji per slide, ONLY for decoration, NEVER in titles/subtitles. Use emoji as visual aids (🍎 for apples, 🐱 for cats) but keep text clean. Validate with grep: ensure no emoji in heading tags or kicker spans.

- **Home button pattern**: For decks needing quick navigation return, add a fixed home button (🏠 or SVG home icon) positioned left of prev/next buttons. Use `data-goto="0"` to jump to first slide. Keep same elegance as arrow buttons (same size, shadow, hover effects).

- **Elegant arrow navigation**: Replace simple circle buttons with SVG icon buttons. Use thin stroke arrows, subtle shadow, smooth hover transform. Size: 56x56px minimum. Active state: accent border or slight scale up. Disabled state: reduced opacity.

- **MyStyle1 design system** (UPDATED 2026-08-23): Inter font, colors #0f172a/#ffffff/#f97316/#f8fafc, NO GRADIENT backgrounds. App Title: UPPERCASE 56-72px (800 ExtraBold). Chapter Dividers: 96-120px (900 Black) full-bleed orange. Minimal emoji: max 1 per slide, ONLY decoration, NEVER in titles. Elegant nav: SVG arrow icons (56px+), home button required. Scroll support: active slides can scroll when content is dense. See `references/myStyle1-design-system.md` for full spec.

- **SD-level content patterns**: For elementary school presentations, simplify language, use concrete examples (fruits, animals, food), larger visuals, fewer emojis. See `references/sd-level-content-patterns.md` for full guidelines.

- Stray placeholder attributes (`style2="\\""`) survive silently after templating —
  grep for `[a-z]+2="\\""`-style artifacts after generating markup, but flag EMPTY
  values only: SVG shapes legitimately carry `x2="168"`/`y2="90"` geometry attrs,
  which false-positive on a naive value-agnostic grep.
- Chrome (progress bar, dots, HUD pills) lives OUTSIDE the `<section>` elements, so
  a section's inline `style="--accent:…"` never cascades to `.dot.active` or bar
  gradients. In `paint()`, push it to the root:
  `document.documentElement.style.setProperty("--accent", accent)`; for two-stop
  progress-bar gradients give each section a `data-grad="#hex1,#hex2"` attribute
  and split it in JS.
- Animated width meters (`width:0 → .active width:X%`) render invisible under
  prefers-reduced-motion overrides — add explicit `width:X%!important` rules to
  that media block.
- Hex-alpha suffix tricks (`accent+"33"` for translucent borders) require
  6-digit hex accents everywhere.
- `color-mix(in srgb, var(--accent) 12%, #fff)` gives free accent tints
  (2023+ browsers); set a solid fallback line before it. CRITICAL: implement
  that fallback as a DOUBLE DECLARATION, never as an `@supports not (...)`
  block nested inside the rule — at-rules are illegal inside declaration
  blocks and silently break parsing of every declaration after them.
  Unsupported `color-mix()` lines are dropped on their own, so:
  ```css
  /* right  */ .rbtn{background:#eef2ff;background:color-mix(in srgb,var(--accent) 9%,#fff)}
  /* wrong  */ .rbtn{background:color-mix(...);@supports not (...){background:#eef2ff}}
  ```
  Same pattern for any color-mix property (border-color, gradient stops).
- Put JS in ONE `<script>` at end of body, wrapped in
  `(function(){ "use strict"; … })();`.
- Long text slides: use the Scrollable Active Slides v5 pattern (slide-level
  scroll + `.inner` measurement + hint) so nothing ever clips on short viewports.
- Multi-agent workspaces (`hermes/elon/` runs several subagents): a sibling
  can overwrite your exact deliverable path MID-SESSION — the patch/write
  tool will warn that the file changed under you. Do NOT blindly rewrite —
  re-inspect the on-disk file against the brief, rerun this validation suite
  on it, ADOPT it if fully compliant (report the collision honestly), restore
  your own build only if it fails spec or validation. Then commit & push
  promptly so the winner is durable. **Always check `git status --short`
  before committing to avoid duplicate work.**
- Render-testing deep links: navigating the browser to `deck.html#7` while the
  deck is ALREADY open is a same-document hash change — no load event fires and
  the deck has no hashchange listener, so you silently stay on the old slide
  while the URL bar reads #7. Run `location.reload()` in the console first,
  THEN verify counter/chip/active heading.
- Reading `slide.scrollTop` immediately after assigning it returns 0 when the
  slide has `scroll-behavior:smooth` — the assignment starts an animation and a
  synchronous read returns the pre-animation position. Wait ~600–800ms before
  asserting scroll position in console tests, or working scroll looks broken
  (v5 cost a debugging round-trip to this).
- Iterative patch → browser_navigate → test loops: the browser may serve CACHED
  html for the same URL, so you debug stale JS (symptom: a listener you just
  added "doesn't fire" while older new code works). Bust cache with a changing
  query param per iteration (`deck.html?v=fix2#N`).
- `.inner` vertical centering with scrollable slides: `justify-content:center`
  combined with `overflow-y:auto` CLIPS the top of overflowing content even when
  scrolled to top (classic flexbox overflow bug). Use auto-margin centering
  instead: drop justify-content, add
  `.inner>*:first-child{margin-top:auto}` and
  `.inner>*:last-child{margin-bottom:auto}` — centers short content, flows
  naturally when tall, never clips.
- Preserving JS across a redesign can carry silent dead features: v1 of the rasio
  deck had an `#svg17` chart div that NO init call ever drew — that slide shipped
  with an empty card its whole life. The usual check (`$('id')` references ⊆
  defined ids) does NOT catch orphaned containers, because the id EXISTS in
  markup while nothing references it. Audit in the other direction too: list
  every chart/container id in markup and confirm each appears in an init or
  update call before shipping the restyle.
- Hex-alpha fallback colors from the old palette can survive a recolor inside
  inline styles (v2 caught a leftover pink `#fda4af` slider-bar fallback). After
  any palette swap, grep the final file for every old-palette hex, not just the
  primary ones.
- Console test scripts: capture each state snapshot into a STRING immediately
  after the action. If the "before" sample holds live element refs
  (`st.className`, `st.textContent`) that are only evaluated when the return
  object literal is built — i.e. AFTER later dispatched mutations — it silently
  reports the AFTER state and the log looks impossible (flow=1 + warn). One
  mixed sample cost a debugging round-trip on the EduApp2 labs. `snap(tag)`
  helpers that stringify on the spot are immune.
- Remote browser sessions can reset to `about:blank` BETWEEN tool calls: a
  console expression that worked moments ago starts throwing `Cannot read
  properties of null` on `document.getElementById(...)`. Check `location.href`
  first — if you're on about:blank the APP didn't break; re-navigate to the
  file URL and re-run the test. Don't "fix" a phantom bug that only exists in
  a reset session.
- When restyling an app shell (EduApp2 pattern), the `window-frame` div must
  WRAP all slides inside `.stage-area`, with `.inner` inside each slide becoming
  flex-column (height:100%) so slides fill the window height rather than
  overflowing. The JS `go()` / `paint()` calls that touch `.innerHTML` or query
  the slide count must still work — verify `slides.length` matches spec after
  restructuring markup. A missing closing `</div>` for `.window-frame` silently
  swallows the last slide.
- Dark-theme desktop shells (EduApp2 v2) require inverting text colors across
  the ENTIRE deck — `--text-primary` becomes light (#f8fafc), `--card-bg`
  becomes dark (#1e293b), `--card-border` becomes mid-tone (#334155). Grep for
  any hardcoded `#0f172a` or `#ffffff` in inline styles BEFORE committing;
  replace with token references so the restyle doesn't leak old palette colors.
  Also strip brand-label strings like "EDUAPP2" or "EduApp2" from visible UI
  (title bar, sidebar footer, frame-top kicker) unless the brief explicitly
  requests them — they become stale artifacts after the v2 redesign.

## Starter Template

Copy `templates/slide-deck-skeleton.html` — a minimal known-good 3-slide deck
(chrome, dots, keyboard/swipe/hash navigation, reveal stagger, print +
reduced-motion) and replace content per slide. For a Modern Professional
(no-gradient, single-accent) look, swap in the styling layer from
`templates/design-system-modern.css` — the validated token sheet shipped in
`rasio-perbandingan-v2.html` (it also carries legacy aliases `--grad-ot`/`.grad`
so gradient-era markup re-renders cleanly during a token-swap restyle).

## Session Reference

- `references/orange-teal-deck.md` — session notes from the 29-slide Rasio & Perbandingan deck (2026-08-23), covering the orange-teal color choice, PPT-scale typography decisions, and validation results.
- `references/modern-professional-tokens.md` — validated token bank from the v2 Modern Professional restyle (2026-08-23): exact palette hexes, Inter weight/type ladder, component treatments (cards/badges/tables/sliders/quiz states), no-gradient cover spec, and viewport-fit ladders.
- `references/scrollable-slides-v5.md` — validated scrollable-active-slide pattern from the v5 revision (2026-08-23): CSS/JS snippets, the `.inner`-measurement rule for needs-scroll detection, scroll-hint injection, scroll-first keyboard map, reveal auto-scroll, and the render-test matrix. Use when labs/quiz content overflows viewport.
- `references/desktop-app-shell-eduapp2.md` — validated desktop-application shell from EduApp2 (2026-08-24): topbar + collapsible sidebar chrome, tech-frame cards, sidebar↔deck sync, collapse mechanics (desktop width vs mobile overlay), the BUTTON keyboard-guard split, and the console-driven lab/quiz state-machine test recipe. Use when the brief asks for a desktop-style app layout instead of a presentation deck.
- `references/modern-split-pane-desktop.md` — validated Modern Split-Pane Desktop pattern (2026-08-24): dark sidebar (#09090b) + light workspace (#fafafa), 2-Tone headings, desktop-card style, FAB navigation. Use when the brief references taraka.id/AGENTS/ui.txt or asks for "desktop app" aesthetic.