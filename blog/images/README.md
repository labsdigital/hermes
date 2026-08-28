# Placeholder untuk gambar blog

Folder ini menyimpan gambar-gambar yang digunakan di artikel blog.

## Struktur

```
blog/images/
├── README.md          # Dokumentasi ini
├── example-image.png  # Contoh gambar
└── ...
```

## Cara Upload

1. Salin gambar ke folder ini:
```bash
cp /path/to/image.png /opt/data/hermes/blog/images/
```

2. Commit dan push:
```bash
cd /opt/data/hermes
git add blog/images/
git commit -m "Blog: Add image for article"
git push origin main
```

3. Gunakan URL:
```
https://raw.githubusercontent.com/labsdigital/hermes/main/blog/images/nama-gambar.png
```

## Format yang Didukung

- PNG (recommended untuk ilustrasi)
- JPG/JPEG (untuk foto)
- SVG (untuk diagram)
- GIF (untuk animasi)

## Best Practices

- Maks ukuran file: 500KB
- Gunakan nama file yang deskriptif
- Tambahkan watermark jika perlu
- Kompress sebelum upload
