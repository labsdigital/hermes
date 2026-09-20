---
name: chalbi-workflow
description: "Chalbi Rumi article writer with email and FTP deploy."
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux]
tags: [subagent, rumi, masnavi, email, ftp, article]
---

# Chalbi Workflow - Rumi Article Writer

## Overview
Chalbi adalah subagent spesialis penulis artikel tentang Jalaluddin Rumi dan Masnavi.

## Workflow (GitHub-First)

### 1. Terima Request
User memberikan topik tentang Rumi/Masnavi.

### 2. Query API Rumi
```bash
curl "https://masnavi.ai/api/search_meaning?q=cinta&limit=10"
```

### 3. Generate Ilustrasi (jika diperlukan)
```bash
export PATH="/opt/data/.local/bin:$PATH"
polli gen image "<prompt artistik detail>" --model klein --output chalbi/reports/gambar.png
```

### 4. Tulis Artikel dengan Poin Hikmah
- Kutipan asli Persia/Arab HARUS disertakan
- Section "Poin Hikmah" di akhir dengan 5-8 point + emoji
- Minimal 800-1000 kata
- Gunakan URL gambar: `https://taraka.id/hermes/chalbi/gambar.png`

### 5. Publish (URUTAN PENTING)
```bash
# Step 1: Commit & push GitHub dulu (gambar harus ada di GitHub sebelum email)
bash chalbi/scripts/commit_article.sh nama-file.md

# Step 2: Publish workflow - update URLs → FTP upload → kirim email
bash chalbi/scripts/publish_article.sh nama-file.md --email
```

## Email Format
- Subject: Full title ONLY (no prefixes)
- Body: HTML dengan `<img>` tag (URL GitHub raw)
- Recipient: tamimnasa.chalbi@blogger.com

## Referensi API
- API: https://masnavi.ai/api/