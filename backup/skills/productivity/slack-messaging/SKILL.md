---
name: slack-messaging
description: Send messages to Slack via Hermes gateway.
version: 1.0.0
author: hermes-agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [slack, messaging, notifications, cron-delivery]
    homepage: https://hermes-agent.nousresearch.com/docs/
---

# Slack Messaging via Hermes Agent

## Setup — Dua Token Diperlukan

Hermes Slack adapter menggunakan **Socket Mode**, jadi butuh dua token:

| Variabel | Prefix | Fungsi |
|----------|--------|--------|
| `SLACK_BOT_TOKEN` | `xoxb-...` | API calls (kirim pesan, baca channel) |
| `SLACK_APP_TOKEN` | `xapp-...` | Socket Mode connection (websocket listener) |
| `SLACK_SIGNING_SECRET` | *(plain)* | Verifikasi request dari Slack |

Semua diset di `~/.hermes/.env`:

```
SLACK_BOT_TOKEN=xoxb-...
SLACK_SIGNING_SECRET=...
SLACK_APP_TOKEN=xapp-...
```

### Verifikasi Token

```bash
# Test bot token
curl -s "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer xoxb-..."

# Test app token
curl -s "https://slack.com/api/auth.test" \
  -H "Authorization: Bearer xapp-..."
```

- Bot token: harus `ok: true`, biasanya 40+ karakter setelah `xoxb-`
- App token: `ok: true`, `app_name` adalah nama Slack app Anda
- Jika `invalid_auth` → token salah/terpotong, bukan masalah prefix

### Restart Gateway Setelah Menambah Token

⚠️ **Jangan restart dari dalam gateway process** — akan di-blok:
> "Refusing to restart the gateway from inside the gateway process"

Cara yang benar:
```bash
# 1. Kill process lama
kill <gateway_pid>

# 2. Start ulang
/opt/hermes/bin/hermes gateway run &
# atau dari shell luar:
/opt/hermes/bin/hermes gateway restart
```

## Kirim Pesan

### hermes send (CLI)

```bash
# Ke home channel
hermes send -t slack "Pesan test"

# Ke specific channel
hermes send -t slack:#channel-name "Halo!"

# Ke DM user
hermes send -t slack:U0123ABCD "Pesan pribadi"

# Dengan subject/header
hermes send -t slack:#engineering --subject "[CI] Build Failed" --file build.log

# Attachment/gambar
hermes send -t slack:#channel "MEDIA:/tmp/chart.png"
```

Format target: `slack`, `slack:#channel`, `slack:U0123ABCD`, `slack:C0123ABCD:thread_ts`

### Dari Cron Job

Gunakan `hermes send -t slack:#channel-name` di prompt cron job. Target otomatis dari `.env`.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `invalid_auth` pada bot token | Token salah/terpotong | Cek token lengkap di Slack API dashboard |
| `invalid_auth` pada app token | Token salah | Verify dengan `curl auth.test` |
| Gateway tidak connect | App token belum diset | Tambah `SLACK_APP_TOKEN=xapp-...` ke `.env` |
| `Refusing to restart` | Restart dari dalam gateway | Kill manual + start ulang |
| `No messaging platforms configured` | Channel belum discover | Jalankan `hermes send --list` setelah setup |

## Minimal Slack App Permissions (Bot Scopes)

- `chat:write`
- `channels:history`, `channels:read`
- `im:history`, `im:read`, `im:write`
- `files:read`, `files:write`
- `users:read`

Socket Mode juga perlu di-enable di Slack App settings.
