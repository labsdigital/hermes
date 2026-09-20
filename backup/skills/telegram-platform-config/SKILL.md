---
name: telegram-platform-config
description: "Configure Telegram bot with user restrictions for Hermes."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [Telegram, Platform, Config, Privacy, multi-bot]
    related_skills: [hermes-agent]
---

# Telegram Platform Configuration

Configure Telegram bot with security restrictions.

## Security Best Practices

**Always restrict access** - Never leave `allow_all_users: true`:

```yaml
platforms:
  telegram:
    enabled: true
    token: "YOUR_BOT_TOKEN"
    allow_all_users: false
    allowed_users:
      - "YOUR_TELEGRAM_USER_ID"
```

## Finding Your User ID

Check channel_directory.json:
```bash
cat /opt/data/channel_directory.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['platforms']['telegram'][0]['id'])"
```

## Configuration

### Edit config.yaml
Location: `/opt/data/config.yaml`

### Or use environment variables
Location: `/opt/data/.env`
```bash
TELEGRAM_BOT_TOKEN=7949893437:***
TELEGRAM_ALLOWED_USERS=5066659725
```

## Multi-Bot Setup (Multiple Telegram Bots)

### Option 1: Multi-Bot in Single Gateway (Default Profile)
Configure multiple bots in the same gateway instance:

```bash
# Set bots array with all tokens
hermes config set platforms.telegram.bots '[
  {"token": "BOT1_TOKEN", "username": "bot1", "allowed_users": ["USER_ID"]},
  {"token": "BOT2_TOKEN", "username": "bot2", "allowed_users": ["USER_ID"]}
]'

# Remove old single token field if exists
hermes config unset platforms.telegram.token
```

### Option 2: Separate Profile per Bot (Recommended for Subagents)
Each bot gets its own profile with isolated gateway:

```bash
# 1. Create profile directory and config
mkdir -p /opt/data/profiles/irfan/platforms/telegram
cat > /opt/data/profiles/irfan/config.yaml << 'EOF'
platforms:
  telegram:
    enabled: true
    bots:
      - token: "NEW_BOT_TOKEN"
        username: irfan
        allowed_users:
          - 'USER_ID'
    allow_all_users: false
  api_server:
    enabled: false
delegation:
  model: stealth/ox-alpha
  provider: openrouter
model:
  provider: openrouter
  default: stealth/ox-alpha
onboarding:
  seen:
    profile_build_offered: true
EOF

# 2. Create wrapper script
cat > /opt/data/home/.local/bin/irfan << 'SCRIPT'
#!/bin/bash
exec /opt/hermes/.venv/bin/hermes -p irfan "$@"
SCRIPT
chmod +x /opt/data/home/.local/bin/irfan

# 3. Start gateway (run from OUTSIDE the gateway process)
/opt/hermes/.venv/bin/hermes -p irfan gateway run --replace
```

**Critical:** Gateway must be started from a SEPARATE process, not from within the running gateway. Use `background=true` in terminal tool or run in a new shell.

## Restart Gateway

**In Docker/s6 container environment:**
```bash
# Use s6-svc to restart the service
s6-svc -dx /run/service/gateway-default  # Stop
s6-svc -u /run/service/gateway-default   # Start
```

**Alternative: Kill and restart**
```bash
# Get PID from gateway list
hermes gateway list
# Kill the process
kill <PID>
# Start new gateway (from OUTSIDE the gateway process)
/opt/hermes/.venv/bin/hermes gateway run --replace
```

**CRITICAL:** Never run restart commands FROM within the gateway process itself. The gateway will kill child processes before they complete. Always run from a separate shell or use background=true in terminal tool.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Bot not responding | Check user ID matches allowed_users |
| Token invalid | Test with `curl https://api.telegram.org/bot<TOKEN>/getMe` before configuring |
| Config not applied | Check YAML indentation, use `hermes config get` to verify |
| Token rejected by server | Verify token is active at @BotFather → /mybots |
| Multiple bots needed | Use separate profiles OR multi-bot config in default |
| Gateway won't restart | Run from OUTSIDE gateway process, use s6-svc or separate shell |
| Bot shows as "not running" | Check gateway.pid file and logs in profile directory |

## Token Validation (Always Do First)

Before configuring ANY bot token, validate it:

```bash
# Test if token is valid
curl -s "https://api.telegram.org/bot<TOKEN>/getMe" | python3 -m json.tool

# Expected output if valid:
# {
#   "ok": true,
#   "result": {
#     "id": 123456789,
#     "is_bot": true,
#     "first_name": "BotName",
#     "username": "bot_username"
#   }
# }

# If "ok": false, token is invalid or expired
```

**Common pitfall:** Token in `.env` may differ from config. Always verify which token is actually being used by checking `hermes config get platforms.telegram`.

## Important Notes

- **Never commit tokens to git** - Use `.env` and `.gitignore`
- **User IDs are numeric** - Not usernames
- **Multiple users** - Use array: `["id1", "id2"]`
- **Token validation** - Test token with `curl https://api.telegram.org/bot<TOKEN>/getMe`
