---
name: atlas-email-workflow
description: "Publish Atlas essays: GitHub, FTP, email, HTML conversion."
version: 1.2.0
author: Hermes Agent + labsdigital
license: MIT
tags: [atlas, essay, email, ftp, html, workflow]
related_skills: [chalbi-workflow, ftp-deploy-pattern, brian-tracy-style]
---

# Atlas Email Workflow

Complete publish pipeline for Atlas non-fiction essays.

## Actual Workflow (2026-09-12 — Updated)

`publish_article.py` consolidates multiple steps. **Do NOT run manual `git add/commit/push` for .md/.html before calling it** — the script already does this and will create a duplicate commit.

### Sequence of Operations

**Step 1 — Call `publish_article.py` ONCE with the article filename (no extension):**
```bash
# Internally: MD→HTML conversion + git add + git commit + git push (for .md and .html only)
python3 hermes/atlas/scripts/publish_article.py <artikel-name>-YYYY-MM-DD --agents
```

**Step 2 — FIX HTML Image URLs (CRITICAL):**
```bash
# Check for duplicate https bug
grep "https://https://" atlas/reports/*.html

# Fix if found
sed -i 's|https://https://|https://|g' atlas/reports/<file>.html

# Commit fix
cd /opt/data/hermes && git add atlas/reports/*.html && git commit -m "Atlas: Fix duplicate URL in HTML" && git push origin main
```

**Step 3 — Push to agents repo + VERIFY all 4 assets:**
```bash
python3 hermes/scripts/push_to_agents.py <artikel-name>-YYYY-MM-DD

# MANDATORY: Verify all 4 assets are on GitHub
FILENAME="<artikel-name>-YYYY-MM-DD"
for f in "$FILENAME.md" "$FILENAME.html" "${FILENAME}.svg" "${FILENAME}-artistik.png"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" "https://raw.githubusercontent.com/labsdigital/agents/main/atlas/reports/$f")
  echo "$f: $code"
done
# All must return 200. If SVG returns 404, manually fix:
#   cd /tmp/agents-clone && cp /opt/data/hermes/atlas/reports/<file>.svg atlas/reports/
#   git add atlas/reports/<file>.svg && git commit -m "Atlas: Add SVG" && git push origin main
```

**Step 4 — Upload all files to FTP:**
```bash
cd /opt/data
python3 hermes/shared/ftp_upload.py hermes/atlas/reports/<artikel-name>-YYYY-MM-DD.md /atlas/
python3 hermes/shared/ftp_upload.py hermes/atlas/reports/<artikel-name>-YYYY-MM-DD.html /atlas/
python3 hermes/shared/ftp_upload.py hermes/atlas/reports/<artikel-name>-diagram.svg /atlas/ 2>/dev/null || true
python3 hermes/shared/ftp_upload.py hermes/atlas/reports/<artikel-name>-artistik.png /atlas/ 2>/dev/null || true
```

**Step 5 — Send email:**
```bash
# Default recipient
python3 hermes/atlas/scripts/send_email.py --article hermes/atlas/reports/<artikel-name>-YYYY-MM-DD.md

# Custom recipient
EMAIL_RECIPIENT=user@example.com python3 hermes/atlas/scripts/send_email.py --article hermes/atlas/reports/<artikel-name>-YYYY-MM-DD.md
```

### Key Pitfalls

- **`polli` not on PATH after `npm i -g @pollinations/cli@latest`:** If `which polli` returns empty, use `npx @pollinations/cli@latest` as a fallback — it works identically and is the observed workaround in this environment.
- **Do NOT manually `git add *.md *.html` before `publish_article.py`** — it creates a duplicate commit. Run Step 1 first, then push to agents in Step 3.
- **`push_to_agents.py` creates TWO commits if called before `publish_article.py`** — first for PNG/SVG, then MD/HTML overwrites them. Always run `publish_article.py --agents` FIRST.
- **`push_to_agents.py` may omit SVG** — Verify all 4 assets after push. If SVG is 404 on GitHub raw, manually copy to `/tmp/agents-clone/` and commit separately. This was observed on 2026-09-03 even though the script claims to handle all 4 types.
- **After `push_to_agents.py`, hermes repo may diverge from origin** — run `git pull --rebase && git push origin main` to sync.
- **SVG files: no XML declaration** — strip `<?xml version="1.0"?>` from any SVG before embedding or uploading. Email clients reject SVG with XML declaration.
- **Email script fallback SVG**: `send_email.py` hardcodes `assets/atrofi-kognitif-illustration.svg` as fallback. SVG/PNG in `atlas/reports/` are NOT auto-selected by the email script — only the HTML version has the correct embedded diagram URL (from `publish_article.py`).
- **Image URLs**: Use `https://labsdigital.github.io/hermes/atlas/reports/` (GitHub Pages), NOT raw GitHub URLs.
- **Article MD must include image references (CRITICAL)**: `publish_article.py` does NOT auto-inject images. The MD must explicitly contain `![Ilustrasi Artistik](...)` at the top and SVG diagram block before conclusion. Without these, HTML will have no images. See references/article-image-references.md for full pattern.
- **polli outputs JPEG despite .png extension**: `polli gen image` produces JPEG binary (`\xff\xd8\xff\xe1`) even when output ends in `.png`. This is cosmetic — GitHub serves correctly at `.png` URL. See references/article-image-references.md for details.
- **HTML image URL duplicate https bug**: `publish_article.py` may create URLs like `https://https://...`. Fix with: `sed -i 's|https://https://|https://|g' atlas/reports/<file>.html`
- **Custom email recipient**: Use environment variable: `EMAIL_RECIPIENT=user@example.com python3 atlas/scripts/send_email.py --article <file>.md`
- **HTML post-generation fix**: After `publish_article.py`, always verify and fix double https in image URLs before declaring completion. Run: `grep "https://https://" atlas/reports/*.html` to check.

## Cron Schedule (2026-08-31 — Updated)
Atlas daily articles run **four times per day** at:
- **07:00 WIB** (00:00 UTC)
- **11:00 WIB** (04:00 UTC)
- **15:00 WIB** (08:00 UTC)
- **19:00 WIB** (12:00 UTC)

Job ID: `0a6777778f4f`
Schedule: `0 0,4,8,12 * * *`

## Key Fixes (2026-08-27 to 2026-09-12)
- SVG inline rendered in HTML, replaced with [Diagram SVG] in plain text
- Title only in Subject line (no duplication)
- No hardcoded illustration in email header
- **2026-08-31**: `push_to_agents.py` FIXED — now copies ALL 4 file types (MD/HTML/PNG/SVG) in single command
- **2026-08-31**: Cron updated to 4x daily (07:00, 11:00, 15:00, 19:00 WIB)
- **2026-08-31**: Image URLs now use `https://labsdigital.github.io/hermes/atlas/reports/` (GitHub Pages hermes)
- **2026-09-12**: HTML image URL duplicate https bug identified and fix pattern added

## SVG Rendering Fix (Critical)
**Problem**: SVG with XML declaration (`<?xml version="1.0"?>`) fails to render in email clients and some browsers.

**Solution**: Strip XML declaration before embedding in HTML:
```python
# In md_to_html(), when processing SVG blocks:
if line.strip().startswith('<?xml'):
    continue  # Skip XML declaration
```

**Why**: Email clients (Gmail, Outlook) and some browsers reject SVG with XML declaration for security reasons.

## Title Duplication Fix
**Problem**: `<h1>` appears twice - once in header, once in article body.

**Solution**: Skip `<h1>` and subtitle lines during body conversion:
```python
# Skip title - already in header
if line.startswith('# ') and not title:
    title = line[2:].strip()
    continue  # Don't add to body

# Skip subtitle line (e.g., "*Esai | Agustus 2026*") - redundant with header
if line.strip().startswith('*Esai') or line.strip().startswith('*Esai '):
    continue
```

## Chalbi Dual Recipient Pattern
Chalbi emails send to TWO recipients by default:
1. `tamimnasa.chalbi@blogger.com` (primary/blog)
2. `tamimnasa@gmail.com` (secondary/personal)

Usage:
```bash
python3 chalbi/scripts/send_email.py --article chalbi/reports/<file>.md
# Sends to both recipients automatically
```

Custom single recipient:
```bash
python3 chalbi/scripts/send_email.py --article <file>.md --recipient user@example.com
```

## Agent-Specific Email Scripts
Each agent has its own email script:
- Atlas: `atlas/scripts/send_email.py` → sends to `tamimnasa.simbioma@blogger.com`
- Chalbi: `chalbi/scripts/send_email.py` → sends to dual recipients

**Rule**: Only call agent's own email script when explicitly asked. Do NOT call atlas script for chalbi articles (and vice versa).

## Git Sync Pattern (New 2026-08-29)
After `push_to_agents.py` runs, hermes repo may have local commits that diverge from origin:

```bash
# Check status
cd /opt/data/hermes && git status

# If diverged, fix with:
git pull --rebase && git push origin main

# If merge conflicts, resolve and continue:
git rebase --continue
```

## Push to Agents Repo Pattern (Updated 2026-09-03)
**`push_to_agents.py` behavior:**
1. Copies `.md`, `.html`, `.png` to `/tmp/agents-clone/atlas/reports/`
2. Commits and pushes to `labsdigital/agents`
3. **Automatically updates `index.html`** with new article link
4. Only commits if there are actual changes (no empty commits)

⚠️ **Known issue**: SVG file may be omitted even though the script claims to handle all 4 types. Always verify all 4 assets are accessible via GitHub raw URLs after push.

**Usage:**
```bash
python3 hermes/scripts/push_to_agents.py <filename>
# Then verify: for f in md html svg png; do curl -s -o /dev/null -w "%{http_code} $f\n" "https://raw.githubusercontent.com/labsdigital/agents/main/atlas/reports/<filename>.$f"; done
```

## Writing Styles Available

### Harari Style (Default)
- Grand synthesis, defamiliarization, narrative-driven
- Third-person perspective (eagle view)
- Long chapters (300-500 words)
- Philosophical depth

### Brian Tracy Style (Alternative)
- Micro-chapters (100-200 words each)
- Problem → Solution → Action Steps formula
- Imperative commands ("Write!", "Start!", "Eliminate!")
- Repeated metaphor anchor (e.g., "Frog" for difficult tasks)
- Zero-fluff, direct to action

See `brian-tracy-style` skill for details.