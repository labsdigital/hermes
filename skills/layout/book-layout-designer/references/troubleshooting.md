# Pemeriksaan Visual & Pemecahan Masalah

Jalankan build dengan `--preview`, lalu buka setiap `sheet_*.jpg` di `out/preview-pdf/` dan `out/preview-docx/`.
Untuk melihat satu halaman lebih detail: `pdftoppm -jpeg -r 90 -f 12 -l 12 buku.pdf hal` lalu buka gambarnya.

## Daftar periksa sebelum menyerahkan
- [ ] Sampul: judul tidak tertabrak ilustrasi, subjudul ≤ 3 baris, chip/sorotan muat.
- [ ] Daftar isi: semua entri bernomor halaman; urutan sesuai isi.
- [ ] Pembuka bagian: kartu tujuan & daftar template tidak keluar halaman (maks. ±5 tujuan, ±12 butir).
- [ ] Tidak ada diagram/gambar terbelah; keterangan gambar ikut bersama gambarnya.
- [ ] Tidak ada label callout atau judul subbab yang tertinggal sendirian di dasar halaman.
- [ ] Tabel: kolom pertama tidak terlalu sempit, tidak ada kata terpotong di tengah.
- [ ] Tidak ada halaman nyaris kosong yang tidak disengaja (lihat di bawah).
- [ ] DOCX: teks judul besar tidak terpotong, gambar tampil utuh, daftar isi terisi, font sesuai tema.
- [ ] Fakta, angka, dan nama di naskah sudah diperiksa (layout bagus tidak menolong isi yang keliru).

## Masalah umum

| Gejala | Penyebab | Perbaikan |
|---|---|---|
| Diagram/tabel pindah ke halaman berikut dan menyisakan ruang kosong besar | Elemen tidak boleh terbelah dan tidak muat | Wajar sesekali. Jika mengganggu: pindahkan paragraf pendek sebelum/sesudahnya, perkecil diagram, atau pecah tabel |
| Satu halaman hanya berisi 2–5 baris sisa tabel/daftar | Konten sedikit melebihi halaman | Ringkas teks sebelumnya, atau beri `{nobreak}` pada bab berikut agar mengisi halaman itu |
| Kolom tabel pertama sangat sempit | Lebar otomatis mengikuti panjang teks | Tambah `{widths=20,40,40}` atau gunakan `{.matrix}` |
| Judul di footer terpotong "…" | Judul bagian > 48 karakter | Isi kolom ke-4 `@part N \| Judul \| Sub \| Judul pendek` |
| Nomor daftar isi kosong (PDF) | Judul bab mengandung karakter yang berbeda di bookmark | Build ulang; pastikan judul tidak mengandung markdown (`**`) |
| Nomor daftar isi DOCX kosong | LibreOffice tidak tersedia saat build | Normal — Word mengisinya saat pengguna memilih "update fields"; atau pasang LibreOffice lalu build ulang |
| Teks judul besar di DOCX terpotong/menumpuk | Spasi baris "exact" | Sudah ditangani `docx_post.py`; jika DOCX diedit ulang dengan alat lain, jalankan ulang `docx_post.py` |
| Font DOCX berbeda dari PDF | Build dengan `--no-embed`, atau dibuka di Google Docs | Build tanpa `--no-embed`; Google Docs memang tidak memakai font embed |
| Garis tipis gelap di dasar halaman sebelum sampul belakang | Artefak Chromium saat berganti *named page* | Sudah ditangani (latar sampul di `::before`); jangan memindahkan latar ke elemen `section` |
| Diagram HTML kosong/tanpa warna di DOCX | Snapshot gagal (fragmen error) | Buka `out/_build/book.html` di Chromium, periksa fragmen; pastikan tidak memuat skrip/eksternal |
| Diagram melebar keluar halaman di A5/B5 | Lebar tetap > lebar isi | Pakai diagram kit (lebar cair) atau `max-width:100%`; zoom otomatis diterapkan untuk A5/B5 |
| `render_pdf.js failed` / Chromium tidak ditemukan | Playwright belum punya browser | `npx playwright install chromium`, atau set `CHROMIUM_PATH=/path/ke/chrome` |
| `Cannot find module 'docx'` | Paket npm belum terpasang | `npm install -g docx playwright` (build.py otomatis menambahkan `npm root -g` ke NODE_PATH) |
| Warna aksen sulit dibaca | Tema kustom gagal kontras | `python scripts/check_contrast.py tema.json` dan sesuaikan |
| Sorotan kuning muncul di teks yang bukan isian | Teks memakai `[kurung siku]` dengan huruf kecil | Tulis ulang tanpa kurung siku, atau `highlight_placeholders: false` |

## Catatan teknis (untuk yang ingin mengubah skrip)
- Chromium tidak mendukung `target-counter()`, jadi daftar isi dibangun dua pass: render → baca bookmark PDF
  (`pages.py outline`) → render ulang dengan nomor halaman.
- Bookmark PDF berasal dari `<h1>` (bab & pembuka bagian) dan `<h2>` (bersarang).
- `figure.fig` harus `display:block`; jika elemen flex, Chromium mengabaikan `break-inside: avoid`.
  Diagram kit ada di dalam `.fig-body` (inline-block) agar tata letak flex-nya tetap bekerja.
- DOCX: pembuka bagian = tabel satu sel berwarna; Heading 1 di dalam sel tetap masuk daftar isi Word.
  Font di-embed dengan obfuscation ECMA-376 (`docx_post.py`); `w:embedTrueTypeFonts` ditambahkan ke settings.
