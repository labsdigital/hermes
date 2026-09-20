---
name: automated-news-summarizer
description: "Fetch RSS, filter, summarize, push to GitHub."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [RSS, News, Automation, GitHub]
    related_skills: [github-repo-management, blogwatcher]
---

# Automated News Summarizer

Fetch RSS feeds from multiple sources, filter for topic-relevant articles, generate summaries, and push to GitHub.

## Core Workflow

### 1. Configure RSS Feeds

```python
FEEDS = [
    ("Source Name", "https://example.com/feed/"),
]
```

### 2. Fetch and Parse Feeds

Handle RSS 2.0 (`<item>`) and Atom (`<entry>`) namespaces:

```python
from urllib.request import urlopen
import xml.etree.ElementTree as ET

with urlopen(url, timeout=10) as response:
    root = ET.fromstring(response.read().decode('utf-8'))
    for item in root.findall('.//item') or root.findall('.//entry'):
        title = item.findtext('title') or item.findtext('{http://www.w3.org/2005/Atom}title')
```

### 3. Filter by Keywords

Deduplicate by title, filter by relevance keywords.

### 4. Generate Summary

Markdown report with date, sources, numbered articles, trend summary. Use Indonesian when user prefers Bahasa Indonesia.

### 5. Push to GitHub

```bash
git pull --rebase origin main
git push origin main
```

## Scheduling

For Jakarta time (WIB = UTC+7):
```cron
0 0 * * *   # 00:00 UTC = 07:00 WIB
```

## Pitfalls

- RSS feeds may use different namespaces (`<item>` vs `<entry>`)
- Same story appears in multiple feeds — deduplicate by title
- Always use `git pull --rebase` before push to avoid conflicts
- Check memory for language preference before generating summaries

## Scripts

- `scripts/ai_news_summarizer.py` — Complete implementation with multi-source RSS fetching, keyword filtering, Indonesian summary generation, and GitHub push