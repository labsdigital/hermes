---
name: cron-script-pattern
description: "Fix cron model drift with no_agent=true and shell scripts."
version: "1.0.0"
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [cron, script, no_agent, model_drift, automation]
    related_skills: [ai-news-automation, hermes-agent]
---

# Cron Script Pattern

Use `no_agent=true` with shell scripts to avoid model drift errors in cron jobs.

## Problem

Cron jobs created with explicit model/provider settings fail when the global inference config changes:
```
RuntimeError: Skipped to prevent unintended spend: global inference config drifted...
```

## Solution

Use `no_agent=true` with a script file:

```bash
# 1. Create script in ~/.hermes/scripts/
cat > ~/.hermes/scripts/my_task.sh << 'EOF'
#!/bin/bash
# Your script here
cd /opt/data
python3 scripts/generate_github_news.py > output.md
git add output.md
git commit -m "Update" && git push origin main
EOF
chmod +x ~/.hermes/scripts/my_task.sh

# 2. Create or update cron job
cronjob action=create \
  name="My Task" \
  schedule="0 0 * * *" \
  script="my_task.sh" \
  no_agent=true \
  workdir="/opt/data"
```

## Git Safety Pattern

Always use stash/rebase to avoid conflicts:

```bash
git stash || true
git pull --rebase origin main || true
git stash pop || true
git commit -m "Update" || echo "No changes"
git push origin main
```

## Script Location

Scripts MUST be in `~/.hermes/scripts/` (relative path only):
- ✅ `script="push_github_news.sh"`
- ❌ `script="/opt/data/scripts/push_github_news.sh"`

## Common Use Cases

### Push to GitHub
```bash
#!/bin/bash
python3 script.py > output.md
cd /path/to/repo
git add output.md
git stash || true
git pull --rebase origin main || true
git stash pop || true
git commit -m "Update: $(date '+%Y-%m-%d %H:%M')" || echo "No changes"
git push origin main
```

### Send to Slack
```bash
#!/bin/bash
source /path/to/.env
export SLACK_BOT_TOKEN SLACK_APP_TOKEN
python3 script.py
```

### Daily Report
```bash
#!/bin/bash
python3 generate_report.py >> /path/to/log.txt
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| Script not found | Check path is in `~/.hermes/scripts/` |
| Model drift error | Use `no_agent=true` |
| Git conflict | Use stash/rebase pattern |
| Permission denied | `chmod +x script.sh` |