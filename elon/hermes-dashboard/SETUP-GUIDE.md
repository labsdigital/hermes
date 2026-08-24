# 🔐 Hermes Dashboard - Setup Guide untuk Shared Hosting

## ⚠️ PENTING: Masalah Jaringan

Dashboard Anda ada di **shared hosting** (luar VPS), tapi Hermes Gateway ada di **VPS** (localhost:9119).

**Solusi yang tersedia:**

### ✅ Opsi 1: expose Hermes Gateway ke Internet (Recommended)

Buka port 9119 di VPS Anda agar bisa diakses dari external hosting:

```bash
# Di VPS Anda, setup reverse proxy dengan Nginx/Caddy
# Contoh dengan Nginx:
sudo nano /etc/nginx/sites-available/hermes

# Isi dengan:
server {
    listen 80;
    server_name hermes.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:9119;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Enable
sudo ln -s /etc/nginx/sites-available/hermes /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

Lalu di `config.php`:
```php
define('HERMES_API_URL', 'https://hermes.yourdomain.com');
```

---

### ✅ Opsi 2: Gunakan Tunnel (Cepat & Mudah)

Gunakan [ngrok](https://ngrok.com/) atau [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/) untuk expose localhost:

```bash
# Dengan ngrok
ngrok http 9119

# Atau dengan cloudflared
cloudflared tunnel --url http://localhost:9119
```

Dapat URL seperti: `https://abc123.ngrok.io`

Lalu di `config.php`:
```php
define('HERMES_API_URL', 'https://abc123.ngrok.io');
```

⚠️ **Catatan:** Tunnel gratisan bersifat temporary (berubah setiap restart).

---

### ✅ Opsi 3: Deploy Dashboard di VPS Juga (Paling Simpel)

Upload dashboard ke VPS yang sama dengan Hermes:

```bash
# Di VPS
cd /opt/data/hermes/elon
cp -r hermes-dashboard /var/www/html/
# Atau symlink
ln -s /opt/data/hermes/elon/hermes-dashboard /var/www/html/hermes-dashboard
```

Lalu akses: `http://your-vps-ip/hermes-dashboard/`

---

### ✅ Opsi 4: WebSocket Polling (No Direct API Access)

Jika gateway TIDAK bisa diakses dari external hosting, ubah arsitektur:

1. **Dashboard** → polling ke VPS via SSH/exec
2. Atau **VPS** push updates ke dashboard via webhook

Ini lebih kompleks, perlu custom development.

---

## 📝 Langkah Setup

### 1. Pilih Opsi di Atas

Pilih salah satu solusi jaringan di atas.

### 2. Edit config.php

```bash
# Di shared hosting, edit file ini:
nano /hermes-dashboard/config.php

# Ubah baris ini:
define('HERMES_API_URL', 'https://hermes.yourdomain.com'); // ← GANTI!
```

### 3. Upload ke Shared Hosting

```bash
# Via FTP/cPanel File Manager
Upload folder: hermes-dashboard/
Ke directory: public_html/hermes-dashboard/
```

### 4. Set Permissions

```bash
# Via SSH di shared hosting (jika ada)
chmod 755 /hermes-dashboard/
chmod 755 /hermes-dashboard/api/
chmod 755 /hermes-dashboard/data/
chmod 600 /hermes-dashboard/data/users.json
```

### 5. Generate Password Hash

```bash
# Via PHP di shared hosting
php -r 'echo password_hash("your_password", PASSWORD_BCRYPT);'

# Copy hasilnya ke data/users.json
```

### 6. Test Access

```
https://yourdomain.com/hermes-dashboard/
```

Login dengan:
- Username: `tamim`
- Password: `hermes2024`

---

## 🔑 Credentials yang Dibutuhkan

| Item | Value | Keterangan |
|------|-------|------------|
| **Hermes API URL** | `https://hermes.yourdomain.com` | Gateway URL (Ops 1) atau Tunnel URL (Ops 2) |
| **API Key/Token** | Kosongkan dulu | Nanti bisa diisi jika gateway pakai auth |
| **Username** | `tamim` | Default admin |
| **Password** | `hermes2024` | Default password (HARUS diganti!) |

---

## 🔒 Security Checklist

- [ ] Ganti default password setelah login pertama
- [ ] Enable HTTPS di shared hosting
- [ ] Set `FORCE_HTTPS = true` di config.php
- [ ] Backup `data/users.json` secara berkala
- [ ] Restrict access via .htaccess (jika pakai Apache)

---

## 📞 Troubleshooting

### Error: "Unauthorized"
→ Hermes gateway butuh auth token. Isi `HERMES_API_TOKEN` di config.php.

### Error: "Connection refused"
→ Gateway URL salah atau firewall memblokir. Cek URL di config.php.

### Error: "Network error"
→ Shared hosting blocks outbound curl. Kontak support hosting.

---

## 🚀 Rekomendasi

**Untuk pemula:** Gunakan **Opsi 3** (deploy di VPS yang sama). Paling simpel.

**Untuk production:** Gunakan **Opsi 1** (reverse proxy) + HTTPS.

**Untuk testing cepat:** Gunakan **Opsi 2** (ngrok).

---

Butuh bantuan? Chat via Telegram: @zetta
