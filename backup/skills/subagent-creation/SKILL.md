---
name: subagent-creation
description: "Create subagents with AGENTS.md structure and GitHub push."
version: 1.2.0
author: Hermes Agent + labsdigital
license: MIT
tags: [subagent, agent, delegation, multi-profile, telegram]
---

# Subagent Creation Pattern

Pola pembuatan subagent terstruktur.

## Struktur
```
project/subagent-name/
├── AGENTS.md
├── skills/<name>/SKILL.md
└── output/reports/
```

## AGENTS.md Wajib
- Nama & peran
- Bahasa (default: Indonesia)
- Kemampuan 3-5 poin
- Workflow langkah demi langkah

## Contoh Max
```bash
mkdir -p hermes/max/{skills/research-writer,reports}
```

## Best Practices
1. Output terstruktur + tanggal
2. Auto-push ke GitHub
3. Bahasa konsisten (Indonesia)

## Multi-Profile Setup (untuk Bot Telegram)
Untuk subagent dengan bot Telegram terpisah:

```bash
# 1. Buat profile
hermes profile create <nama> --description "<role>"

# 2. Konfigurasi Telegram
hermes config set --profile <nama> platforms.telegram.token "<BOT_TOKEN>"
hermes config set --profile <nama> platforms.telegram.allow_all_users false
hermes config set --profile <nama> platforms.telegram.allowed_users.0 "<USER_ID>"

# 3. Konfigurasi model
hermes config set --profile <nama> model.provider openrouter
hermes config set --profile <nama> model.default stealth/ox-alpha

# 4. Set API key
echo "OPENROUTER_API_KEY=<key>" >> /opt/data/profiles/<nama>/.env

# 5. Start gateway
<path>/gateway start
```

**Penting:** 
- Bot token perlu validasi dengan @BotFather. Token yang expired/rejected akan error di gateway logs.
- Jika token ditolak server ("The token was rejected by the server"), revoke di @BotFather lalu buat token baru.
- Gunakan `hermes config get --profile <nama> platforms.telegram` untuk cek konfigurasi.
- Pairing code dari user perlu diapprove: `<alias> pairing approve telegram <CODE>`

## Atlas Subagent (Essay Writer)

Atlas subagent untuk essay writing dengan Bot Telegram sendiri:
- Profile: `/opt/data/profiles/atlas/`
- Bot: @atlas46114bot (token: 8896649752:AAH0vq5VbH-gbSq-4L4sv7iaBJMvVfeptUQ)
- Model: stealth/ox-alpha via OpenRouter
- Pairing: Disetujui untuk Tamim (5066659725)
- Output: `/opt/data/hermes/atlas/reports/`
- Gateway: Running di port terpisah

## Related
- `delegate-task`
- `github-push-workflow`
- `telegram-platform-config`

## See Also
- `references/atlas-setup.md` — Atlas subagent setup guide dengan Telegram bot