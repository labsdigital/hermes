# EduApp2 Template

Template standar untuk aplikasi pembelajaran interaktif bergaya desktop.

## Struktur Folder
```
elon/eduapp2-template/
├── index.html      # Template utama (30 slides)
├── README.md       # Dokumentasi ini
└── USAGE.md        # Panduan penggunaan
```

## Fitur Template
- ✅ 30 slides (6 bab)
- ✅ Sidebar navigasi dengan progress tracking
- ✅ Window frame desktop style
- ✅ Dark navbar + light content
- ✅ Quiz system (template ready)
- ✅ Canvas simulation placeholder
- ✅ Responsive mobile design
- ✅ Keyboard & touch swipe navigation
- ✅ Print-friendly

## Cara Menggunakan

### 1. Copy Template
```bash
cp elon/eduapp2-template/index.html elon/[nama-proyek]/index.html
```

### 2. Edit Bagian Berikut:
- **Line 1**: `<title>` — ganti dengan judul aplikasi
- **Line 161**: `.tb-title` — ganti `[JUDUL APLIKASI]`
- **Line 169**: `.sb-title` — ganti dengan judul
- **Line 171**: `.sb-sub` — ganti dengan subjek
- **Line 180-280**: Sidebar navigation — sesuaikan jumlah slide & label
- **Line 300+**: Slide content — isi dengan materi pembelajaran
- **Line 800+**: JavaScript — tambahkan quiz data & simulation logic

### 3. Commit & Push
```bash
cd /opt/data/hermes
git add elon/[nama-proyek]/
git commit -m "Elon: [Nama Aplikasi] — EduApp2 Template"
git push origin main
```

### 4. GitHub Pages
Aplikasi akan tersedia di:
```
https://labsdigital.github.io/hermes/elon/[nama-proyek]/
```

## Konvensi Slide (30 Slides)

| Slide | Bab | Konten |
|-------|-----|--------|
| 1 | Pengenalan | Hero/Cover |
| 2-3 | Pengenalan | Definisi & Komponen |
| 4-8 | Teori | Konsep 1-5 + Rumus |
| 9-14 | Lab | 6 Lab Interaktif |
| 15-17 | Latihan | 3 Contoh Soal |
| 18-20 | Latihan | 3 Set Latihan (5 soal tiap) |
| 21-25 | Evaluasi | 5 Kuis Bab (5 soal tiap) |
| 26 | Evaluasi | Kuis Penutup (10 soal) |
| 27-29 | Penutup | Rangkuman + 2 Misi |
| 30 | Penutup | Selamat! |

## Customization Checklist

- [ ] Ganti semua `[JUDUL APLIKASI]` dengan judul proyek
- [ ] Ganti semua `[SUBJEC]` dengan nama subjek
- [ ] Update sidebar navigation (slide count & labels)
- [ ] Isi konten setiap slide
- [ ] Tambahkan quiz data ke `QUIZ_DATA` object
- [ ] Implementasikan simulation canvas (jika perlu)
- [ ] Test di browser sebelum commit
- [ ] Push ke GitHub

## Referensi
- Contoh implementasi: `elon/gerak-parabola/`
- Contoh CT v3: `elon/computational-thinking-v3/`
