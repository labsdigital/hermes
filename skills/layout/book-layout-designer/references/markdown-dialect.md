# Dialek Markdown Buku

Semua komponen ditulis di file `.md` biasa. Urutan file mengikuti `chapters` di `book.yaml`
(glob diurutkan alfabetis, jadi beri awalan `00-`, `01-`, …).

## Daftar isi
1. Struktur: bab, bagian, subjudul
2. Teks & inline
3. Daftar & langkah
4. Callout
5. Kotak template & blok kode
6. Tabel
7. Gambar & diagram (diagram kit)
8. Lain-lain
9. Kerangka bab yang direkomendasikan

---

## 1. Struktur

### Bab (chapter)
```markdown
# Pengantar
# Lampiran A · Glosarium
# Peta Perjalanan {nobreak}
# Catatan Internal {notoc}
# Ucapan Terima Kasih {kicker="BAGIAN AWAL"}
```
- Selalu mulai halaman baru, kecuali `{nobreak}`.
- Kicker otomatis: "BAGIAN AWAL" sebelum bagian inti pertama, "PENUTUP & LAMPIRAN" setelah bagian terakhir.
  Judul berpola `Lampiran X · Judul` / `Appendix X · Title` otomatis memakai kicker "LAMPIRAN X".
- `{notoc}` menyembunyikan bab dari daftar isi.
- Daftar isi disisipkan setelah sampul, atau setelah bab yang disebut di `toc_after`.

### Bagian inti (part / modul / bab besar)
```markdown
@part 3 | RPP & Diferensiasi | Satu tujuan, beberapa jembatan | RPP & Diferensiasi

:::goals
- Menyusun draf RPP ...
- Menerapkan pola CRA ...
:::
```
Format: `@part NOMOR | Judul | Subjudul | Judul-pendek-footer` (dua kolom terakhir opsional).
Alias: `@modul`, `@bab`, `@chapter`. Label di halaman pembuka diambil dari `part_label` di `book.yaml`.

Halaman pembuka otomatis berisi: label + nomor besar, judul, subjudul, kartu **tujuan** (dari `:::goals`
/`:::tujuan` tepat setelah `@part`) dan kartu **template di bagian ini** (dari kotak template di
bagian itu) — atau daftar subjudul `##` jika tidak ada template.

### Subjudul
```markdown
## 1. Friksi Nyata di Ruang Guru      → angka "1" menjadi lencana berwarna aksen
## Tanpa Nomor                        → subjudul biasa
### A. Kerangka TRACE                  → subjudul tingkat 3
```

## 2. Teks & inline
- Paragraf: baris berurutan digabung; pisahkan paragraf dengan baris kosong.
- `**tebal**`, `*miring*`, `` `kode` ``, `[teks](https://tautan)`.
- `[variabel isian]` (mengandung huruf kecil, > 2 karakter) disorot kuning sebagai isian. Tag huruf besar
  seperti `[VERIFIKASI]` dan angka rujukan `[1]` tidak disorot. Matikan semua sorotan dengan
  `highlight_placeholders: false`.
- Komentar HTML `<!-- ... -->` di awal baris diabaikan.

## 3. Daftar & langkah
```markdown
- butir
  - sub-butir (indentasi 2 spasi)
1. langkah
2. langkah

{.steps}
1. **Baca pembuka** untuk melihat tujuan.
2. **Pahami prinsip** lewat diagram.
```
`{.steps}` mengubah daftar bernomor menjadi garis waktu dengan lingkaran nomor (di DOCX tampil sebagai daftar bernomor biasa).

## 4. Callout
```markdown
:::tip Mulai dari asesmen
Tentukan bukti keberhasilan lebih dulu.
- boleh berisi daftar, tabel, dll.
:::

:::warning{label="KESELAMATAN KERJA"} Gunakan sarung tangan
Label bawaan bisa diganti dengan atribut label.
:::
```

| Jenis (alias) | Warna | Gunakan untuk |
|---|---|---|
| `note` (catatan, info) | primer | informasi tambahan, konteks |
| `tip` (tips) | hijau | saran praktis |
| `analogy` (analogi) | aksen | analogi/metafora penjelas |
| `policy` (kebijakan, regulasi) | biru | rujukan regulasi, panduan resmi |
| `warning` (perhatian, peringatan) | merah | risiko, larangan |
| `limits` (uji, batasan) | merah | keterbatasan/kritik atas pendekatan |
| `check` (koreksi, praktik) | hijau | praktik baik, koreksi |
| `privacy` (privasi) | netral gelap | data pribadi, keamanan |
| `exercise` (latihan) | aksen | tugas praktik |
| `question` (refleksi, dilema) | ungu | pertanyaan diskusi/refleksi |
| `example` (contoh) | biru | contoh kasus |
| `summary` (intisari, ringkasan) | kotak gelap | ringkasan akhir bab; paragraf terakhir tampil sebagai "kalimat kunci" |
| `card` (kartu) | garis putus | kartu ringkas untuk dicetak/digunting |
| `quote` (kutipan) | garis aksen | kutipan besar; judul = sumber kutipan |
| `goals` (tujuan) | — | hanya setelah `@part` |
| `stats` (angka) | kartu angka | lihat di bawah |

```markdown
:::stats
- 8 | Modul inti
- 25 | Template siap pakai
- 70 | Halaman
:::
```
Gunakan 2–4 kartu. Nilai sebaiknya pendek (angka atau 1–2 kata).

**Batas wajar**: maksimal 2 callout berturut-turut; callout > 12 baris lebih baik dipecah atau dijadikan subbagian biasa.

## 5. Kotak template & blok kode
````markdown
```prompt Template 2.1 · Wawancara Balik
### PERAN
Bertindaklah sebagai ...
- Jenjang: [SMP Kelas 8]
Tandai klaim yang ragu dengan [VERIFIKASI].
```

```python contoh.py
print("halo")
```
````
- `prompt` atau `template` → kotak template: judul `Template 2.1 · Judul` dipecah menjadi chip
  "TEMPLATE 2.1" dan judul. `### LABEL` di dalamnya menjadi subjudul kecil. Isi lain tampil apa adanya
  (spasi awal dipertahankan) sehingga mudah disalin.
- Bahasa lain (`python`, `bash`, `json`, …) → blok kode dengan chip nama bahasa.

## 6. Tabel
Tabel pipe standar. Baris atribut `{...}` tepat sebelum tabel memilih gaya dan lebar kolom.
```markdown
{.dodont widths=20,40,40}
| Aspek | Lakukan | Hindari |
|---|---|---|
| Tujuan | Kata kerja operasional | Kata kerja kabur |
```

| Gaya | Efek |
|---|---|
| (tanpa) | header warna primer, baris zebra, lebar kolom otomatis |
| `.dodont` | kolom 2 header hijau "✓", kolom 3 header merah "✗", kolom 1 tebal |
| `.compare` | dua kolom sebelum (merah) vs sesudah (hijau) |
| `.matrix` | kolom 1 tebal & 20%, kolom lain sama lebar (contoh lintas jenjang) |
| `.key` | kolom 1 tebal |
| `.glossary` | 26/74, kolom istilah tebal |
| `.checklist` | kolom nomor & kotak centang di tengah |
| `.numbered` | kolom 1 berupa nomor berwarna aksen |
| `widths=a,b,c` | lebar relatif kolom (angka bebas, dinormalkan) |

Tabel panjang boleh terpotong halaman; header diulang otomatis dan baris tidak pernah terbelah.

## 7. Gambar & diagram
```markdown
@figure figures/alur.html | Gambar 1.1 Alur merancang modul
@figure img/foto.jpg | Gambar 2.3 Suasana kelas | width=70%
@figure img/grafik.svg | Gambar 3.1 Tren nilai
```
Path relatif terhadap file markdown. Semua gambar dibungkus bingkai yang **tidak terbelah halaman**.
HTML/SVG dirender vektor di PDF dan di-*screenshot* ke PNG untuk DOCX; PNG/JPG dipakai langsung.

### Diagram kit
Tulis fragmen HTML (tanpa `<html>`/`<body>`) memakai kelas berikut. Warnanya otomatis mengikuti tema
(`var(--primary)`, `var(--accent)`, `var(--s0)`…`var(--s4)` = palet seri). Lebar standar 640px.

**Alur langkah** (`dk-flow`; tambah kelas `hi` untuk menyorot satu langkah):
```html
<div class="dk"><div class="dk-flow">
  <div class="dk-step"><div class="dk-n">1</div><div class="dk-title">Tujuan</div><div class="dk-desc">siapa, apa, kriteria</div></div>
  <div class="dk-step hi"><div class="dk-n">2</div><div class="dk-title">Aktivitas</div><div class="dk-desc">pengalaman belajar</div></div>
  <div class="dk-step"><div class="dk-n">3</div><div class="dk-title">Asesmen</div><div class="dk-desc">bukti belajar</div></div>
</div><div class="dk-note">Keterangan kecil di bawah diagram</div></div>
```
**Chevron proses** (`dk-chev`, 3–5 langkah):
```html
<div class="dk"><div class="dk-chev">
  <div><div class="dk-k">LANGKAH 1</div><div class="dk-title">Data nyata</div><div class="dk-desc">tabel, grafik</div></div>
  <div><div class="dk-k">LANGKAH 2</div><div class="dk-title">Trade-off</div><div class="dk-desc">variabel bersaing</div></div>
  <div><div class="dk-k">LANGKAH 3</div><div class="dk-title">Keputusan</div><div class="dk-desc">pertahankan pilihan</div></div>
</div></div>
```
**Kartu pilar** (`dk-cards`, 2–5 kartu, lingkaran huruf opsional):
```html
<div class="dk"><div class="dk-cards">
  <div><div class="dk-L">T</div><div class="dk-title">Task</div><div class="dk-desc">Luaran apa?</div></div>
  <div><div class="dk-L">R</div><div class="dk-title">Role</div><div class="dk-desc">Keahlian apa?</div></div>
</div></div>
```
**Corong** (`dk-funnel`, baris pertama abu-abu, `class="end"` untuk hasil akhir):
```html
<div class="dk"><div class="dk-funnel">
  <div>Semua kemungkinan jawaban</div><div>+ Task → luaran spesifik</div><div>+ Role → sudut pandang</div>
  <div class="end">Draf yang cocok untuk kelas Anda</div>
</div></div>
```
**Rumah/pilar** (`dk-pillars`):
```html
<div class="dk dk-pillars"><div class="dk-roof">TUGAS TAHAN AI</div>
  <div class="dk-cols"><div><div class="dk-title">Konteks lokal</div><div class="dk-desc">data sekolah</div></div>
  <div><div class="dk-title">Proses</div><div class="dk-desc">jurnal, revisi</div></div></div>
  <div class="dk-base">Fondasi: penilaian proses</div></div>
```
**Sebelum vs sesudah** (`dk-vs`):
```html
<div class="dk"><div class="dk-vs">
  <div><div class="dk-tag">SEBELUM</div>Prompt satu baris</div><div class="dk-arrow">→</div>
  <div><div class="dk-tag">SESUDAH</div>Prompt TRACE lengkap</div>
</div></div>
```
**Siklus** (`dk-cycle` + `dk-loop`):
```html
<div class="dk"><div class="dk-cycle">
  <div><div class="dk-h">FEED UP</div><div class="dk-b"><div class="dk-title">Ke mana?</div><div class="dk-desc">kriteria</div></div></div>
  <div><div class="dk-h">FEED BACK</div><div class="dk-b"><div class="dk-title">Di mana posisi?</div><div class="dk-desc">bukti</div></div></div>
  <div><div class="dk-h">FEED FORWARD</div><div class="dk-b"><div class="dk-title">Langkah berikut?</div><div class="dk-desc">1–2 aksi</div></div></div>
</div><div class="dk-loop"><span>siklus berulang</span></div></div>
```
Butuh bentuk lain? Tulis SVG sendiri di dalam fragmen (pakai `currentColor` atau warna tema) atau
tambahkan `<style>` di fragmen. Uji dengan build lalu lihat pratinjau: teks harus terbaca pada lebar 640px.

## 8. Lain-lain
- `@pagebreak` — paksa pindah halaman (gunakan hemat; biasanya tidak perlu).
- Konten sebelum bab pertama dianggap pengantar tanpa judul.
- Front matter YAML (`---` … `---`) di awal file diabaikan.

## 9. Kerangka bab yang direkomendasikan
Untuk modul pelatihan/panduan praktis, pola berikut terbukti mudah dipindai:
```markdown
@part N | Judul | Subjudul
:::goals ... :::
## 1. Masalah Nyata            (paragraf pendek + daftar jebakan)
## 2. Prinsip Kerja            (penjelasan + analogi + diagram)
## 3. Sebelum vs Sesudah       ({.compare})
## 4. Lakukan vs Hindari       ({.dodont})
## 5. Template Siap Pakai      (```prompt ...)
## 6. Contoh Lintas Konteks    ({.matrix})
## 7. Uji Batas                (:::limits + :::check)
## 8. Latihan & Refleksi       (:::exercise + :::question)
## 9. Intisari                 (:::summary, akhiri dengan satu kalimat kunci)
```
Untuk buku naratif/akademik, cukup `##`/`###` dengan callout `note`, `quote`, dan `example` secukupnya.
