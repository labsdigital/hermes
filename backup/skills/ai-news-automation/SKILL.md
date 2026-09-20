---
name: ai-news-automation
description: "Automated AI news pipeline with GitHub and Slack via cron."
version: "1.1.0"
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [RSS, AI, News, GitHub, Slack, Cron, Automation]
    related_skills: [ai-news-digest, slack-messaging, github-repo-management]
---

# AI News Automation

Complete automated pipeline for AI news: fetch RSS feeds, generate markdown summaries for GitHub, send notifications to Slack.

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────┐
│  RSS Feeds  │────▶│ generate_        │────▶│ GitHub      │
│  (TC/Ars)   │     │ github_news.py   │     │ (markdown)  │
└─────────────┘     └──────────────────┘     └─────────────┘
                              │
                              ▼
                       ┌──────────────────┐     ┌─────────────┐
                       │ send_slack_      │────▶│ Slack       │
                       │ news.py          │     │ (#workflows)│
                       └──────────────────┘     └─────────────┘
```

## Scripts

### 1. generate_github_news.py
Generates comprehensive markdown with:
- Date header and timestamp
- Articles grouped by category (Regulasi, Agent, Perusahaan, etc.)
- Indonesian summaries for each article
- Source links

**Usage:** `python3 generate_github_news.py > output.md`

### 2. send_slack_news.py
Sends top 8 new articles to Slack #workflows channel using Block Kit.

**Environment:** Requires `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` from `/opt/data/.env`.

### 3. push_github_news.sh
Orchestrates GitHub push with git stash/rebase pattern.

### 4. send_slack_news.sh
Wraps Slack sender with env loading.

## Cron Configuration

All jobs use `no_agent=true` to avoid model drift issues:

| Job ID | Name | Schedule | Script |
|--------|------|----------|--------|
| `b3255f65ab91` | AI News Daily Summary | 00:00 UTC (07:00 WIB) | push_github_news.sh |
| `3e3fed4f1b29` | AI News - Pagi | 00:00 UTC (07:00 WIB) | send_slack_news.sh |
| `bc8ef7774c81` | AI News - Siang | 06:00 UTC (13:00 WIB) | send_slack_news.sh |

**Create job:**
```bash
cronjob action=create \
  name="AI News GitHub" \
  schedule="0 0 * * *" \
  script="push_github_news.sh" \
  no_agent=true \
  workdir="/opt/data"
```

## Key Patterns

### Avoiding Model Drift
Cron jobs with explicit model settings fail when global config changes. **Solution:** Use `no_agent=true` with shell scripts.

### Git Safety Pattern
```bash
git stash || true
git pull --rebase origin main || true
git stash pop || true
```

### Script Location
Scripts must be in `~/.hermes/scripts/` for cronjob to find them.

### Deduplication
Cache stored at `/opt/data/home/.hermes/ai_news_sent.json`. Articles sent within 30 days are skipped.

## Categories
- 🔒 Regulasi: security, safety, alignment, risk, attack
- 🤖 Agent: agent, browser, autonomous, coding, copilot, cursor
- 🏢 Perusahaan: openai, anthropic, meta, google, deepseek
- ⚖️ Hukum: regulation, law, policy, ethics, governance
- 🧠 Model: llm, gpt, claude, gemini, training, benchmark
- 🎨 Kreatif: video, image, generation, diffusion
- 💰 Bisnis: funding, raise, investment
- ⚡ Hardware: chip, gpu, nvidia, tpu

## File Locations
- Scripts: `~/.hermes/scripts/` (push_github_news.sh, send_slack_news.sh, generate_github_news.py, send_slack_news.py)
- Source: `/opt/data/scripts/` (duplicates for reference)
- Output: `/opt/data/hermes_repo/ai_news_summary.md`
- Cache: `/opt/data/home/.hermes/ai_news_sent.json`
