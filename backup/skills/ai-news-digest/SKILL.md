---
name: ai-news-digest
description: "Auto AI news digest: RSS feeds, Indonesian summaries."
version: "1.0.0"
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [RSS, AI, News, Summarization, GitHub, Automation, Cron]
    related_skills: [github-repo-management]
---

# AI News Digest

Automated pipeline to fetch AI news from RSS feeds, generate comprehensive Indonesian-language summaries, and push to a GitHub repository on a schedule.

## Overview

This skill covers:
- Fetching RSS feeds from AI news sources (TechCrunch, Ars Technica)
- Filtering and categorizing AI-related articles
- Generating comprehensive Indonesian-language summaries
- Pushing results to a GitHub repository
- Scheduling automated daily runs via cron

## Workflow

### 1. Fetch RSS Feeds

```bash
python3 /opt/data/scripts/ai_news_summarizer.py
```

The script fetches from these feeds by default:
- TechCrunch AI: `https://techcrunch.com/category/artificial-intelligence/feed/`
- Ars Technica AI: `https://arstechnica.com/tag/artificial-intelligence/feed/`

### 2. Filter AI Articles

Articles are filtered using keyword detection:
- Core: `ai`, `artificial intelligence`, `machine learning`, `llm`, `gpt`
- Models: `deep learning`, `neural network`, `openai`, `anthropic`, `claude`, `gemini`, `llama`, `deepseek`
- Agents: `ai agent`, `automation`, `chatbot`
- Research: `nlp`, `computer vision`, `robotics`, `transformer`, `benchmark`

### 3. Categorize News

| Category | Indonesian | Keywords |
|----------|-----------|----------|
| Keamanan | Security | security, safety, alignment, risk, attack |
| AI Agent | AI Agent | agent, automation, browser, coding |
| Perusahaan | Company | openai, anthropic, meta, google, deepseek |
| Regulasi | Regulation | regulation, law, policy, ethics, ban |
| Model AI | AI Model | model, llm, gpt, claude, training |
| Pengembangan | Development | code, software, developer, openjdk |
| Sains & Lingkungan | Science | weather, climate, forecast, cyclone |
| Bisnis & Investasi | Business | funding, raise, investment, million |
| Produk | Product | chat, consumer, free, user |

### 4. Generate Summary

The output includes:
- Header with date, sources, article count
- Numbered news items with categories and Indonesian summaries
- Trend analysis section with keyword counts
- Conclusion section
- Methodology section

**Output format:** Markdown file at `{repo}/AI_News_Summary_{DD_Month_YYYY}.md`

### 5. Push to GitHub

The script handles:
- Writing the summary file
- Git add, commit, pull --rebase, push
- Repository: `labsdigital/hermes` (by default)

## Scheduled Execution

Cron job runs daily at **07:00 WIB** (00:00 UTC):

```bash
# Cron schedule
0 0 * * * python3 /opt/data/scripts/ai_news_summarizer.py
```

Job ID: `b3255f65ab91` (AI News Daily Summary)

## Pitfalls

### String Replacement Bug
Simple `replace()` for translation can corrupt words containing the search string. For example:
- `replace('will', 'akan')` corrupts "unlimited" → "unumakan"
- `replace('the', '')` removes "the" from inside other words

**Fix:** Use specific keyword handlers for well-known articles instead of generic translation.

### Git Commit Failures
If the file already exists in the repo, `git add` may fail silently. **Fix:** Remove the file first with `git rm --cached` before regenerating.

### No New Content
If no new AI articles are found, the script exits with code 1. Check RSS feed availability.

## Files

| File | Purpose |
|------|---------|
| `/opt/data/scripts/ai_news_summarizer.py` | Main script |
| `/opt/data/hermes/AI_News_Summary_*.md` | Generated output |
| `/opt/data/.config/himalaya/config.toml` | Email config (optional) |

## References

- See `references/rss-feeds.md` for additional feed URLs
- See `references/category-keywords.md` for complete keyword lists
- See `scripts/ai_news_summarizer.py` for the main automation script
