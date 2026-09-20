---
name: ftp-deploy
description: "Upload files to external hosting via FTP for blog publishing."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
tags: [ftp, deployment, hosting, blog]
---

# FTP Deploy Script

## Overview
Upload files ke hosting eksternal via FTP untuk blog publishing.

## Usage
```bash
# Upload single file
bash upload_to_hosting.sh <file> [remote_path]

# Batch deploy
bash deploy_all.sh
```

## Configuration
Edit script atau set env vars:
```bash
export FTP_HOST="ftp.example.com"
export FTP_USER="username"
export FTP_PASS="password"
export REMOTE_PATH="/public_html/blog/"
```

## Scripts
- `upload_to_hosting.sh` - Upload single file/folder
- `deploy_all.sh` - Batch deploy all articles

## Prerequisites
- Install lftp: `sudo apt-get install lftp`
