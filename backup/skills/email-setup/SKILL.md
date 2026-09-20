---
name: email-setup
description: "Setup email clients for sending emails from Hermes Agent."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Gmail, Setup]
---

# Email Setup for Hermes Agent

This skill covers installing and configuring email clients for sending emails from Hermes Agent sessions.

## Installation

### Himalaya CLI

Himalaya is a modern terminal email client with IMAP/SMTP support.

```bash
# Install to persistent location
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# Verify installation
himalaya --version  # Should show v2.0.0+ with +smtp +gmail +imap

# Add to PATH if needed
export PATH="$HOME/.local/bin:$PATH"
```

## Gmail Configuration

### Step 1: Generate App Password

Gmail requires App Passwords (not regular passwords) for IMAP/SMTP access:

1. Go to https://myaccount.google.com/apppasswords
2. Sign in if prompted
3. Select "Mail" for the app
4. Select "Other (Custom name)" and enter "Hermes Agent"
5. Click "Generate"
6. Copy the 16-character password (format: `abcd efgh ijkl mnop`)

### Step 2: Create Configuration

Create `~/.config/himalaya/config.toml`:

```toml
[accounts.gmail]
email = "your-email@gmail.com"
display-name = "Your Name"
default = true

# IMAP settings (for reading)
backend.type = "imap"
backend.host = "imap.gmail.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "your-email@gmail.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show gmail/app-password"

# SMTP settings (for sending)
message.send.backend.type = "smtp"
message.send.backend.host = "smtp.gmail.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "your-email@gmail.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show gmail/app-password"

# Gmail folder aliases (required!)
folder.aliases.inbox = "INBOX"
folder.aliases.sent = "[Gmail]/Sent Mail"
folder.aliases.drafts = "[Gmail]/Drafts"
folder.aliases.trash = "[Gmail]/Trash"
```

## Common Operations

### Send Email

```bash
# From file
himalaya message send < email.txt

# Using template
cat << 'EOF' | himalaya template send
From: you@gmail.com
To: recipient@example.com
Subject: Test Email

Body text here.
EOF
```

### Read Email

```bash
# List emails
himalaya envelope list

# List with JSON output
himalaya envelope list --output json
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Login failed" | Verify app password is exactly 16 chars without spaces |
| "Authentication required" | Enable 2FA on Google account first |
| Duplicate emails sent | Check folder aliases are correct (use plural `aliases`, not singular `alias`) |
| SMTP connection refused | Verify port 587 is open, check firewall settings |

## Pitfalls

1. **Folder alias syntax**: Use `folder.aliases.X` (plural), NOT `[accounts.NAME.folder.alias]` (singular). The singular form is silently ignored in v1.2.0+.

2. **Retry duplicates**: If `himalaya message send` fails after SMTP delivery, retries will send duplicate emails. Always verify errors before retrying.

3. **Password in config**: Never use `backend.auth.raw` with actual passwords in production. Use `auth.cmd` with a password manager or env var.

## Related Skills

- `himalaya` - Full Himalaya CLI skill for advanced email operations
