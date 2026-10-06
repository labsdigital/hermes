---
name: book-layout-designer
description: Menghasilkan dokumen berlayout buku yang menarik dan mudah dibaca — ebook, modul pelatihan, handbook, panduan, buku ajar, laporan panjang — sebagai PDF dan/atau DOCX dari satu naskah markdown, lengkap dengan sampul, daftar isi otomatis, halaman pembuka bab/modul, callout, kotak template, tabel bergaya, diagram, dan 7 tema warna+tipografi yang sudah diuji kontrasnya. Gunakan skill ini setiap kali pengguna meminta ebook, buku, modul, handbook, panduan, booklet, atau dokumen panjang yang "menarik", "rapi", "profesional", "seperti buku", atau "layout bagus" dalam PDF atau Word, termasuk saat mengubah naskah/DOCX/markdown yang ada menjadi ebook — walaupun pengguna tidak menyebut kata "layout". Use for any request to design or typeset a book-like PDF/DOCX (ebook, training module, guidebook, handbook, long report).
---

# Book Layout Designer

Skill ini mengubah naskah menjadi buku yang **enak dilihat dan enak dibaca**, dalam dua format sekaligus:
**PDF** (dicetak Chromium, presisi tinggi) dan **DOCX** (bisa disunting di Word, font tema ikut ter-*embed*).
Keduanya dibangun dari satu sumber: file markdown berdialek sederhana + `book.yaml`.

Mengapa pipeline, bukan menulis HTML/DOCX manual setiap kali: tata letak buku punya banyak jebakan
(gambar terbelah di batas halaman, label callout yatim, daftar isi tanpa nomor halaman, spasi baris
DOCX yang memotong teks). Semua itu sudah ditangani skrip di `scripts/`. Tugas Anda adalah
**menyusun isi dan struktur yang baik**, lalu memeriksa hasilnya secara visual.

## Kapan dipakai

- Ebook, modul pelatihan, buku ajar, panduan, handbook, SOP bergaya buku, laporan panjang (≥ 8 halaman)
- Mengubah naskah lama (DOCX/PDF/markdown) menjadi ebook yang lebih menarik
- Pengguna meminta "PDF dan Word" dengan tampilan yang sama

Tidak perlu untuk surat, memo satu halaman, atau slide. Untuk dokumen pendek tanpa bab, skill ini tetap
bisa dipakai tanpa `@part` (hanya bab `#`).

## Alur kerja

### 1. Tetapkan struktur, tema, dan format
Putuskan dari isi dan pembacanya:

- **Struktur**: bab awal (`#`: pengantar, cara membaca) → **bagian inti** (`@part`, dapat halaman pembuka penuh)
  → penutup & lampiran (`#` setelah bagian terakhir). Buku tanpa bagian inti juga sah.
- **Tema** (lihat `references/themes.md`):

| Tema | Cocok untuk |
|---|---|
| `edukasi` (teal & amber, Poppins/Lora) | modul pelatihan guru, bahan ajar, panduan pendidikan |
| `korporat` (navy & coral, Outfit/Work Sans) | laporan, whitepaper, SOP, proposal |
| `akademik` (maroon & emas, Crimson Pro) | buku ajar, monograf, bahan kuliah |
| `teknologi` (slate & cyan, Bricolage/Instrument Sans) | dokumentasi teknis, TIK, koding |
| `alam` (hijau & pasir, Work Sans/IBM Plex Serif) | lingkungan, kesehatan, humaniora |
| `premium` (plum & emas, Young Serif/Lora) | kepemimpinan, coaching, katalog |
| `ceria` (biru & kuning, Poppins/Work Sans) | buku anak, LKPD, materi siswa SD |

- **Ukuran halaman**: `A4` (default, cetak kantor), `B5` (terasa seperti buku), `A5` (saku), `Letter`.
- **Bahasa label**: `lang: id` atau `en` (label callout, daftar isi, dsb.).

Jika pengguna tidak menyebut preferensi, pilih tema yang paling sesuai isi dan sebutkan pilihan itu
dalam satu kalimat saat menyerahkan hasil; mengganti tema cukup mengubah satu baris.

### 2. Tulis naskah dalam dialek markdown buku
Baca `references/markdown-dialect.md` sebelum menulis — isinya sintaks lengkap setiap komponen dan kapan memakainya.
Ringkasan komponen:

| Tulis | Hasil |
|---|---|
| `# Judul {kicker="LAMPIRAN A" nobreak notoc}` | Bab baru (halaman baru, kicker kecil + judul besar) |
| `@part 1 \| Judul \| Subjudul \| Judul pendek footer` | Halaman pembuka bagian penuh warna |
| `:::goals` tepat setelah `@part` | Kartu tujuan di halaman pembuka |
| `## 1. Judul` / `### Judul` | Subjudul (angka `1.` otomatis jadi lencana) |
| `:::note/tip/analogy/policy/warning/limits/check/privacy/exercise/question/example Judul` | Callout berwarna (alias Indonesia: catatan, tips, analogi, kebijakan, perhatian, uji, koreksi, privasi, latihan, refleksi, contoh) |
| `:::summary Judul` (alias `intisari`) | Kotak intisari gelap; paragraf terakhir = "satu kalimat untuk diingat" |
| `:::stats` + `- 25 \| label` | Kartu angka kunci |
| `:::quote Sumber` / `:::card` | Kutipan besar / kartu ringkas bergaris putus |
| ` ```prompt Template 1.1 · Judul ` | Kotak template siap salin; `[variabel]` disorot, `### LABEL` jadi subjudul |
| ` ```python judul.py ` | Blok kode |
| `{.dodont}` `{.compare}` `{.matrix}` `{.checklist}` `{.glossary}` `{widths=20,40,40}` sebelum tabel | Gaya tabel |
| `{.steps}` sebelum daftar bernomor | Garis waktu langkah bernomor |
| `@figure figures/x.html \| Gambar 1.1 ...` | Diagram (HTML/SVG/PNG/JPG), aman dari terbelah halaman |
| `@pagebreak` | Pindah halaman |

Prinsip isi yang membuat buku *engaging* (detail di `references/design-system.md`):
- **Ritme visual**: setiap ±1 halaman isi beri satu jangkar visual (callout, tabel, diagram, template).
  Dinding teks > 7 baris dipecah atau diubah menjadi daftar/tabel.
- **Pola bab yang konsisten** membuat pembaca cepat menemukan sesuatu, misalnya:
  masalah → prinsip → contoh sebelum/sesudah → lakukan/hindari → template → latihan → intisari.
- **Satu fungsi, satu komponen**: urutan → daftar bernomor/`{.steps}`; perbandingan → `{.dodont}`/`{.compare}`;
  peringatan → `:::warning`; ringkasan → `:::summary`. Jangan memakai callout sebagai hiasan.
- Diagram ditulis sebagai fragmen HTML memakai **diagram kit** (`dk-flow`, `dk-chev`, `dk-cards`,
  `dk-funnel`, `dk-pillars`, `dk-vs`, `dk-cycle`) yang otomatis mengikuti warna tema — lihat contoh di
  `references/markdown-dialect.md` dan `assets/example/figures/`.

### 3. Tulis `book.yaml`
Salin `assets/example/book.yaml` lalu ubah. Kunci penting: `title`, `subtitle`, `edition`, `author`,
`theme`, `page_size`, `part_label` (Modul/Bab/Bagian/Chapter), `toc_after`, `cover` (motif: `helm`,
`orbit`, `grid`, `waves`, `book`, `none`; `title_lines` untuk memecah judul dengan baris aksen;
`tagline`, `highlights`, `chips`), `back_cover`, `chapters` (daftar/glob file), `output.name`.
`theme_overrides` mengganti warna/font tertentu tanpa membuat tema baru.

### 4. Build
```bash
python scripts/check_env.py                 # sekali di awal: memeriksa Python/Node/Chromium/LibreOffice
python scripts/build.py path/book.yaml --preview
#   --formats pdf|docx|pdf,docx   --theme NAMA   --out DIR   --no-embed (tanpa embed font DOCX)
```
Build menjalankan dua pass agar daftar isi berisi nomor halaman yang benar, mengambil snapshot sampul
dan diagram untuk DOCX, meng-*embed* font tema ke DOCX, dan (dengan `--preview`) menulis lembar kontak
halaman ke `out/preview-pdf/` dan `out/preview-docx/`.

### 5. Periksa hasil secara visual — jangan dilewati
Buka setiap lembar pratinjau (Read gambar `sheet_*.jpg`). Periksa: sampul, daftar isi bernomor,
pembuka bagian, diagram tidak terbelah, tabel tidak meluap, tidak ada halaman nyaris kosong yang
mengganggu, label callout tidak terpisah dari isinya, DOCX tidak memotong teks besar.
Temuan umum dan perbaikannya ada di `references/troubleshooting.md`. Perbaiki, build ulang, periksa lagi.

### 6. Serahkan
Kirim PDF dan/atau DOCX. Sampaikan singkat: tema yang dipakai, jumlah halaman, dan dua catatan DOCX —
(a) Word dapat menanyakan "update fields" saat dibuka (pilih *Yes* agar nomor daftar isi mengikuti
tata letak Word), (b) font tema sudah ter-*embed*, tetapi Google Docs mengabaikan font embed.

## Tema kustom & merek sendiri
Salin tema terdekat di `assets/themes/`, ubah `colors`/`fonts`, lalu jalankan
`python scripts/check_contrast.py path/tema.json` — semua pasangan warna harus lolos (WCAG).
Font tambahan: taruh file TTF berlisensi terbuka di `assets/fonts/` dan daftarkan di `assets/fonts/fonts.json`.
Detail: `references/themes.md`.

## Sumber masukan yang sudah ada
- DOCX: `pandoc input.docx -t markdown --wrap=none -o naskah.md`, lalu susun ulang ke dialek (tabel pipe,
  callout, template). Diagram ASCII di naskah lama sebaiknya dibuat ulang dengan diagram kit.
- PDF: ekstrak teks (`pdftotext -layout`) lalu susun ulang.
- Pertahankan isi pengguna; perbaiki struktur, konsistensi istilah, dan ritme visual.

## File di skill ini
- `scripts/build.py` — satu perintah build (memanggil skrip lain)
- `scripts/parse_md.py`, `render_html.py`, `render_pdf.js`, `snapshot.js`, `render_docx.js`, `docx_post.py`, `pages.py`
- `scripts/check_env.py`, `check_contrast.py`, `preview.py` — cek lingkungan, kontras, pratinjau
- `assets/book.css` — stylesheet buku + diagram kit; `assets/themes/*.json`; `assets/fonts/` (OFL)
- `assets/example/` — contoh buku lengkap (jalankan build-nya untuk melihat semua komponen)
- `references/markdown-dialect.md`, `design-system.md`, `themes.md`, `troubleshooting.md`
