# Deployment: Subdomain vs Subdirectory

## Jawaban Singkat: **BISA KEDUANYA!** ✅

---

## 🎯 Opsi A: Subdirectory (Recommended untuk Pemula)

### Struktur
```
https://yourdomain.com/hermes-dashboard/
```

### Keuntungan
- ✅ Lebih mudah setup
- ✅ SSL sudah ada (ikuti domain utama)
- ✅ Tidak perlu beli domain baru
- ✅ Cocok untuk testing/internal

### Kekurangan
- ⚠️ URL lebih panjang
- ⚠️ Mungkin bentrok dengan route lain

### Cara Setup

**Di Shared Hosting (cPanel):**
```
public_html/
└── hermes-dashboard/
    ├── index.php
    ├── login.php
    ├── config.php
    └── ...
```

**Di VPS dengan Nginx:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    root /var/www/html;
    index index.php;
    
    # Dashboard di subdirectory
    location /hermes-dashboard/ {
        alias /opt/data/hermes/elon/hermes-dashboard/;
        try_files $uri $uri/ /hermes-dashboard/index.php?$query_string;
        
        location ~ \.php$ {
            fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
            fastcgi_param SCRIPT_FILENAME $request_filename;
            include fastcgi_params;
        }
    }
}
```

**Di VPS dengan Apache:**
```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /var/www/html
    
    <Directory /var/www/html/hermes-dashboard>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

---

## 🎯 Opsi B: Subdomain

### Struktur
```
https://dashboard.yourdomain.com/
```

### Keuntungan
- ✅ URL lebih bersih
- ✅ Isolasi lebih baik
- ✅ Bisa SSL terpisah
- ✅ Cocok untuk production

### Kekurangan
- ⚠️ Perlu setup DNS record
- ⚠️ Mungkin perlu SSL certificate terpisah
- ⚠️ Sedikit lebih kompleks

### Cara Setup

**1. Buat DNS Record:**
```
Type: A
Name: dashboard
Value: [IP VPS Anda]
TTL: 3600
```

**2. Setup Web Server:**

**Nginx:**
```nginx
server {
    listen 80;
    server_name dashboard.yourdomain.com;
    
    root /var/www/hermes-dashboard;
    index index.php;
    
    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }
    
    location ~ \.php$ {
        fastcgi_pass unix:/var/run/php/php8.1-fpm.sock;
        fastcgi_param SCRIPT_FILENAME $request_filename;
        include fastcgi_params;
    }
}
```

**Apache:**
```apache
<VirtualHost *:80>
    ServerName dashboard.yourdomain.com
    DocumentRoot /var/www/hermes-dashboard
    
    <Directory /var/www/hermes-dashboard>
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

**3. Install SSL (Let's Encrypt):**
```bash
sudo certbot --nginx -d dashboard.yourdomain.com
# Atau
sudo certbot --apache -d dashboard.yourdomain.com
```

---

## 🎯 Opsi C: Root Domain (Tidak Direkomendasikan)

### Struktur
```
https://yourdomain.com/
```

### Masalah
- ❌ Bentrok dengan website utama
- ❌ Harus replace existing content
- ❠ Rumit setup-nya

**Hanya recommend jika:** Anda punya domain khusus untuk dashboard.

---

## 📊 Perbandingan

| Aspek | Subdirectory | Subdomain |
|-------|--------------|-----------|
| **Kemudahan** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **SSL** | Pakai domain utama | Butuh terpisah |
| **DNS** | Tidak perlu | Perlu A record |
| **Isolasi** | Rendah | Tinggi |
| **Production** | Cukup | Lebih baik |
| **Testing** | Recommended | Optional |

---

## 🎓 Rekomendasi Saya

### Untuk Testing / Internal Use:
**→ Subdirectory** (`yourdomain.com/hermes-dashboard/`)

Alasan:
1. Tidak perlu setup DNS
2. SSL otomatis ikut domain utama
3. Cepat deploy
4. Cocok untuk personal dashboard

### Untuk Production / Public Access:
**→ Subdomain** (`dashboard.yourdomain.com`)

Alasan:
1. Isolasi lebih baik
2. SSL terpisah (lebih aman)
3. URL lebih profesional
4. Mudah scaling nanti

---

## 🔧 Config untuk Masing-Masing

### Subdirectory (tidak perlu ubah config.php):
```php
// config.php - tetap seperti ini
define('HERMES_API_URL', 'https://hermes.yourdomain.com');
```

### Subdomain (jika gateway juga di subdomain):
```php
// config.php
define('HERMES_API_URL', 'https://hermes.yourdomain.com');
// atau
define('HERMES_API_URL', 'http://localhost:9119'); // jika 1 VPS
```

---

## ✅ Checklist Deploy

### Subdirectory:
- [ ] Upload folder ke public_html/hermes-dashboard/
- [ ] Set permissions (755 untuk folder, 600 untuk users.json)
- [ ] Edit config.php (HERMES_API_URL)
- [ ] Test akses: https://yourdomain.com/hermes-dashboard/
- [ ] Login: tamim / hermes2024

### Subdomain:
- [ ] Buat DNS A record (dashboard → IP)
- [ ] Setup web server (Nginx/Apache)
- [ ] Install SSL certificate
- [ ] Upload files
- [ ] Test akses: https://dashboard.yourdomain.com/
- [ ] Login: tamim / hermes2024

---

## 📞 Butuh Bantuan?

Tanyakan di Telegram: @zetta

---

**Kesimpulan:** Bisa subdirectory ATAU subdomain. Pilih sesuai kebutuhan!
