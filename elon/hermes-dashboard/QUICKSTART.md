# Herme(s Dashboard - Quick Start

## 🚀 3 Langkah Setup

### 1. Pilih Cara Akses Gateway

**PILIH SALAH SATU:**

```
[ ] Opsi A: Deploy di VPS yang sama (paling mudah)
[ ] Opsi B: Reverse proxy gateway ke domain
[ ] Opsi C: Gunakan tunnel (ngrok/cloudflare)
[ ] Opsi D: WebSocket polling (advanced)
```

### 2. Edit Configuration

```bash
# Buka file ini:
nano config.php

# Ubah baris ke-12:
define('HERMES_API_URL', 'https://hermes.yourdomain.com');
# Jadi sesuai pilihan Anda di atas
```

### 3. Upload & Test

```bash
# Upload ke shared hosting via FTP/cPanel
# Akses: https://yourdomain.com/hermes-dashboard/
# Login: tamim / hermes2024
```

---

## 📋 Credentials

| Type | Value |
|------|-------|
| **Dashboard Login** | tamim / hermes2024 |
| **Hermes Gateway** | `https://hermes.yourdomain.com` (setting di config.php) |

---

## 🔗 Links

- [Full Setup Guide](SETUP-GUIDE.md)
- [PRD Document](PRD.md)
- [GitHub Repository](https://github.com/labsdigital/hermes)

---

## ⚡ Quick Commands

```bash
# Generate password hash
php -r 'echo password_hash("newpassword", PASSWORD_BCRYPT);'

# Test gateway connectivity
curl -I https://hermes.yourdomain.com

# View logs
tail -f data/logs/*.log
```
