---
name: gen-image
description: "Generate SVG diagrams and PNG images for Hermes blog."
version: 1.0.0
author: atlas
created: 2026-08-28
category: media
---

# Skill: Gen Image

Skill untuk generate gambar SVG dan PNG artistic untuk semua agen Hermes.

## Directory Structure

```
/opt/data/hermes/
├── images/              # Pusat penyimpanan semua gambar
│   ├── atlas/           # Gambar Atlas
│   ├── chalbi/          # Gambar Chalbi
│   ├── max/             # Gambar Max
│   ├── elon/            # Gambar Elon
│   └── taraka/          # Gambar Taraka
├── blog/                # Blog articles
└── scripts/
```

## Usage

### Generate SVG Diagram

```bash
python3 /opt/data/hermes/scripts/generate_svg.py \
  --agent atlas \
  --title "Web Pasca-AI Architecture" \
  --output /opt/data/hermes/images/atlas/
```

Atau buat SVG manual dan simpan ke folder agen.

### Generate PNG Artistic

```bash
export PATH="$PATH:/opt/data/.local/bin"
polli gen image "Futuristic AI web architecture with agent layers" \
  --model klein \
  --output /opt/data/hermes/images/atlas/ai-web-architecture.png
```

## URL Pattern

Semua gambar dipublish ke:
```
https://labsdigital.github.io/hermes/images/{agent}/{filename}
```

Contoh:
- https://labsdigital.github.io/hermes/images/atlas/web-pasca-ai-artistik.png
- https://labsdigital.github.io/hermes/images/chalbi/ridha-illustration.png

## Workflow

1. **Generate gambar** ke `/opt/data/hermes/images/{agent}/`
2. **Commit & push** ke GitHub
3. **Gunakan URL** untuk embed di artikel/blog

## Agents

Semua agen Hermes dapat menggunakan skill ini:
- atlas (purple #667eea)
- chalbi (pink #f093fb)
- max (cyan #64ffda)
- elon (yellow #ffd700)
- taraka (red #e94560)