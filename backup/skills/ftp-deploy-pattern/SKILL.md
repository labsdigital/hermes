---
name: ftp-deploy-pattern
description: "FTP deploy for Hermes agents. Use taraka.id URL."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
tags: [ftp, deploy, upload, hermes, agents]
---

# FTP Deploy Pattern

Use when deploying agent content (articles, apps) to hosting via FTP.

## Problem

The FTP host `ftp.rumahguru.org` returns SSL certificate mismatch errors when accessed via HTTPS.

## Solution

Use `taraka.id/hermes/` as the public web URL.

## Workflow

### 1. Upload via FTP
```bash
python3 /opt/data/hermes/shared/ftp_upload.py <local_file> /<agent>/
```

### 2. Web URL Format
```
https://taraka.id/hermes/<agent>/<filename>
```

### 3. Verify Access
```bash
curl -s -o /dev/null -w "%{http_code}" "https://taraka.id/hermes/<agent>/<file>.md"
# Expect: 200
```

## Agent Paths

| Agent | Web URL Base | Email Script | Notes |
|-------|--------------|--------------|-------|
| chalbi | `https://taraka.id/hermes/chalbi/` | `chalbi/scripts/send_email.py` | Dual recipients by default |
| atlas | `https://taraka.id/hermes/atlas/` | `atlas/scripts/send_email.py` | Single recipient |

## Important Notes
- **SVG**: Strip XML declaration (`<?xml...?>`) before embedding in HTML/email
- **Title Duplication**: Skip `<h1>` in body if already in header
- **Agent Scripts**: Use agent-specific email script only (don't mix atlas/chalbi)
- **When to email**: Only send email when explicitly requested, not automatically

## Example

```bash
bash /opt/data/hermes/chalbi/scripts/commit_article.sh \
  chalbi/reports/article.md --email
# URL: https://taraka.id/hermes/chalbi/article.md
```