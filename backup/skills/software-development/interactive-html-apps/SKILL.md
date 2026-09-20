---
name: interactive-html-apps
description: Use when building single-file interactive HTML web apps.
---

# Interactive HTML Apps (single-file)

Build, browser-verify, and ship self-contained interactive HTML artifacts (learning modules, slide apps, quizzes, labs, demos) — Tailwind/Lucide/Google-Fonts via CDN, vanilla JS, no build step — often against a design-system reference URL, then commit/push into a shared multi-agent repo (e.g. the `elon/` subagent workspace).

## Workflow
1. **Fetch context before writing code.** `curl -sL <design-system-url>` and read the repo's `AGENTS.md` at the workdir — commit-message convention, folder layout, and CDN defaults live there, not in the task prompt.
2. **Commit to a surface archetype and token set first** (see `references/split-pane-desktop-theme.md` for the taraka.id "Modern Split-Pane Desktop" system used across this workspace's education apps — reuse its condensed tokens instead of re-fetching).
3. **Build** as one IIFE; define every `initX()` before calling it at the bottom; keep static HTML placeholders consistent with JS-computed values (see Pitfalls).
4. **Verify in a real browser BEFORE committing** (see `references/browser-verification-recipes.md`):
   - load via `file://`, check console for JS exceptions,
   - run programmatic interaction tests for every lab/quiz/state machine (not just screenshots — clicks reveal logic bugs screenshots never show),
   - vision-screenshot 2–3 representative states.
5. Fix → re-verify → commit with the repo's convention → push. Commit promptly; in multi-agent repos a fast commit shrinks the overwrite race window.

## Pitfalls
- **Missing init function = blank app with no obvious error.** An IIFE that calls an undefined `initQuiz()` dies silently; the shell (sidebar/header) renders but content is empty. Diagnose by evaluating DOM state in the page (count `.active` elements, `innerHTML.length` of each dynamic container) to find which init died, then re-`eval()` the script text in try/catch to capture the real message.
- **Canvas animation not running** — Most common causes: (1) `requestAnimationFrame` called before canvas is sized, (2) delta time calculation wrong, (3) animation loop not restarting after reset. Fix: ensure `canvas.width/height` set BEFORE first draw call. Use `(timestamp - lastTime) / 1000` for delta (seconds), clamp to max 0.05s to prevent spiral on tab-switch. Call `requestAnimationFrame(loop)` at END of loop, not beginning. Verify with `browser_console` expression: `typeof animId === 'number' && animId !== 0`.
- **Programmatic click loops vs. re-rendering DOM.** If the app re-renders a container's `innerHTML` on click (very common with delegated handlers), a loop holding element references clicks *detached* nodes after the first iteration — the delegated listener never fires and your test silently under-selects. Click ONE element, re-query the live DOM, repeat. This trap produces false "app is broken" conclusions.
- **Async browser_console eval:** if you build a promise chain inside `expression`, RETURN the final promise — otherwise the tool returns `null` while the test still ran in the background (then you must read state in a follow-up call).
- **Sibling agent write conflicts in shared repos:** the patch tool warns `modified by sibling subagent ... re-read the file before writing` and anchors stop matching. Re-read the file, decide path ownership (a task-designated output path wins), rewrite the FULL file via write (patch anchors are dead), and commit+push immediately. Check `git log` afterwards — the sibling may have committed its own version that yours supersedes.
- **Placeholder drift:** hardcoded counters in static HTML (e.g. `0 / 16`) that JS immediately overwrites with the real total (e.g. `20`) fail reviews and grep-based checks — make them match.
- **EduApp2 style mismatch:** when user references EduApp2, use desktop-app shell pattern (sidebar + topbar + window frame + light theme), NOT dark theme. The dark theme variant is EduApp2 v2/dark. Always check reference file before coding.

## References
- `references/split-pane-desktop-theme.md` — condensed token/component/interaction spec of the taraka.id "Modern Split-Pane Desktop" theme (colors, sidebar accordion, FAB, transitions, responsive rules).
- `references/browser-verification-recipes.md` — copy-paste recipes: silent-crash diagnosis, sequential click testing for re-rendering DOMs, async console-eval test harness.
