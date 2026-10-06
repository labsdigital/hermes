# Tema

Tujuh tema bawaan, semuanya lolos `scripts/check_contrast.py`. Tema = warna + huruf + ukuran dasar.
Ganti tema cukup dengan `theme: nama` di `book.yaml` atau `--theme nama` saat build.

| Nama | Palet | Suasana & cocok untuk | Judul / Isi | Ukuran isi | Primer · Aksen |
|---|---|---|---|---|---|
| `akademik` | Maroon & Gold | Klasik, berwibawa, cocok untuk buku ajar, monograf, prosiding, bahan kuliah | Crimson Pro / Crimson Pro | 11.3 pt | `#6B1E2E` `#D4AE55` |
| `alam` | Forest & Sand | Tenang, organik, cocok untuk topik lingkungan, humaniora, kesehatan, komunitas | Work Sans / IBM Plex Serif | 9.8 pt | `#2D5A3D` `#E0B458` |
| `ceria` | Biru & Kuning | Ramah, energik, cocok untuk buku anak, LKPD, bahan ajar SD, materi siswa | Poppins / Work Sans | 10.8 pt | `#2446A8` `#FFB627` |
| `edukasi` | Teal & Amber | Hangat, tepercaya, cocok untuk modul pelatihan guru, bahan ajar, panduan pendidikan | Poppins / Lora | 10.2 pt | `#0F4C5C` `#F2A541` |
| `korporat` | Navy & Coral | Profesional, tegas, cocok untuk laporan tahunan, whitepaper, SOP, proposal | Outfit / Work Sans | 9.8 pt | `#1B2F4E` `#F26B4F` |
| `premium` | Plum & Gold | Elegan, eksklusif, cocok untuk buku kepemimpinan, coaching, katalog program, portofolio | Young Serif / Lora | 10.2 pt | `#3F1D38` `#D8A657` |
| `teknologi` | Slate & Cyan | Modern, presisi, cocok untuk dokumentasi teknis, panduan TIK/koding, buku digital | Bricolage Grotesque / Instrument Sans | 9.9 pt | `#1E293B` `#22D3EE` |

Semua tema memakai **JetBrains Mono** untuk template dan kode.

## Memilih tema
- Tanyakan: siapa pembacanya, dan kesan apa yang diinginkan (hangat, tegas, klasik, modern, tenang, eksklusif, ceria)?
- Materi guru/pelatihan → `edukasi`; dokumen organisasi/kantor → `korporat`; bahan kuliah/buku ilmiah → `akademik`;
  TIK/koding/dokumentasi → `teknologi`; lingkungan/kesehatan/sosial → `alam`; program eksklusif/kepemimpinan → `premium`;
  anak/SD/lembar kerja → `ceria`.
- Jika ada warna lembaga, mulai dari tema yang suasananya paling dekat lalu pakai `theme_overrides`.

## Menimpa sebagian tema dari book.yaml
```yaml
theme: korporat
theme_overrides:
  colors:
    primary: "#003B73"      # biru lembaga
    primaryDark: "#00264D"
    accent: "#F5B700"
  fonts:
    body: Lora
  type:
    base: 10.4
```
Setelah menimpa warna, periksa kontras: simpan tema hasil gabungan (ada di `out/_build/theme.json` setelah
build) lalu jalankan `python scripts/check_contrast.py out/_build/theme.json`.

## Membuat tema baru
Salin `assets/themes/edukasi.json` ke nama baru dan ubah nilainya. Struktur:
```json
{
  "name": "lembagaku", "label": "Lembagaku — Biru & Emas", "mood": "…",
  "colors": {
    "primary": "#…", "primary2": "#…", "primaryLight": "#…", "primaryDark": "#…",
    "accent": "#…", "accentDark": "#…", "accentLight": "#…",
    "success": "#…", "successLight": "#…", "danger": "#…", "dangerLight": "#…",
    "info": "#…", "infoLight": "#…", "violet": "#…", "violetLight": "#…",
    "neutral": "#…", "neutralLight": "#…",
    "ink": "#…", "muted": "#…", "line": "#…", "zebra": "#…", "codeBg": "#…", "codeHead": "#…",
    "paper": "#FFFFFF", "series": ["#…", "#…", "#…", "#…", "#…"]
  },
  "fonts": { "heading": "Poppins", "body": "Lora", "mono": "JetBrains Mono" },
  "type": { "base": 10.2, "leading": 1.56, "headingWeight": 700 }
}
```
Aturan praktis:
- `primaryDark` ≈ primary digelapkan 30–40% (untuk gradasi sampul); `primary2` ≈ primary lebih terang/jenuh.
- Versi `Light` = warna dasar dengan kecerahan ±94–97% (latar callout).
- `accent` harus kontras di atas `primaryDark` (≥ 3:1) dan dapat ditulisi teks `ink` (≥ 4,5:1);
  `accentDark` adalah versi aksen yang cukup gelap untuk teks kecil di atas putih.
- `series` = 5 warna berbeda rona, masing-masing lolos teks putih ≥ 4,5:1.
- `headingWeight`: 700 untuk huruf yang punya Bold; 400 untuk huruf display satu bobot (Young Serif).
- Jalankan `python scripts/check_contrast.py assets/themes/lembagaku.json` sampai "ALL PASS".
  Bila gagal, gelapkan warna latar/teks yang disebut sedikit demi sedikit.

## Huruf
Huruf dimuat dari `assets/fonts/` (semua berlisensi SIL Open Font License, file lisensi disertakan) lewat
`assets/fonts/fonts.json`, sehingga PDF tidak bergantung pada huruf terpasang di sistem dan DOCX dapat
meng-*embed* huruf yang sama. Keluarga tersedia: Poppins, Lora, Work Sans, IBM Plex Serif, Crimson Pro,
Outfit, Bricolage Grotesque, Instrument Sans, Young Serif, JetBrains Mono.

Menambah huruf: salin file TTF statis (Regular/Bold/Italic/BoldItalic) berlisensi terbuka beserta file
lisensinya ke `assets/fonts/`, lalu tambahkan entri:
```json
"Nama Keluarga": {"regular": "File-Regular.ttf", "bold": "File-Bold.ttf", "italic": "File-Italic.ttf", "boldItalic": "File-BoldItalic.ttf"}
```
Hindari huruf variabel (satu file untuk semua bobot) untuk DOCX — Word tidak menanganinya dengan baik.
