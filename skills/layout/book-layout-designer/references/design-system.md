# Sistem Desain Buku

Prinsip di balik stylesheet dan tema. Baca saat membuat tema kustom, menilai hasil build, atau
saat pengguna meminta "lebih menarik"/"lebih mudah dibaca". Semua angka di bawah sudah diterapkan
di `assets/book.css`; bagian ini menjelaskan alasannya agar Anda bisa menyesuaikan dengan sadar.

## 1. Tipografi

**Pasangan huruf.** Judul memakai huruf berkarakter (sans geometris atau serif display), isi memakai huruf
yang tenang untuk bacaan panjang. Kontras peran ini membuat hierarki terlihat tanpa perlu banyak warna.

| Tema | Judul | Isi | Alasan |
|---|---|---|---|
| edukasi | Poppins | Lora | sans ramah + serif hangat untuk bacaan panjang |
| korporat | Outfit | Work Sans | bersih dan netral, terasa profesional |
| akademik | Crimson Pro | Crimson Pro | serif klasik buku, satu keluarga = berwibawa |
| teknologi | Bricolage Grotesque | Instrument Sans | grotesk modern + sans rapat, cocok dengan kode |
| alam | Work Sans | IBM Plex Serif | judul lugas, isi serif humanis |
| premium | Young Serif | Lora | serif display elegan untuk judul |
| ceria | Poppins | Work Sans | bulat dan ramah, ukuran isi lebih besar |

**Skala.** Ukuran dasar isi 9,8–11,3 pt tergantung huruf (Crimson Pro kecil secara optis, jadi dasarnya
11,3 pt; huruf sans lebar seperti Work Sans cukup 9,8 pt). Skala turunan: H3 ≈ 1,1×, H2 ≈ 1,42×, judul bab
≈ 2,45×, judul pembuka bagian 25 pt, judul sampul 44 pt. Rasio yang konsisten membuat hierarki terbaca sekilas.

**Spasi baris** 1,5–1,62. Huruf dengan x-height besar (Poppins, Work Sans) butuh spasi lebih lega.
**Panjang baris** ideal 60–80 karakter; margin A4 18 mm menghasilkan ±85 karakter untuk serif 10 pt —
batas atas yang masih nyaman. Untuk bacaan yang sangat panjang, pertimbangkan B5 (±70 karakter).

**Hindari**: teks rata kanan-kiri (sungai spasi), huruf kapital untuk kalimat panjang, lebih dari dua
keluarga huruf (+ monospace), teks isi di bawah 9 pt, dan judul yang dicetak miring.

**Huruf kapital + tracking** hanya untuk label pendek (kicker, label callout, chip): ukuran kecil,
jarak huruf 1,3–4 px, sehingga terasa "label", bukan teks.

## 2. Warna

**Peran warna, bukan daftar warna.** Setiap tema punya peran yang sama sehingga komponen selalu konsisten:
- `primary` / `primaryDark` / `primary2`: identitas — sampul, judul, header tabel, kotak intisari.
- `accent` / `accentDark` / `accentLight`: sorotan — nomor besar, lencana subjudul, chip template, garis aksen.
- `success`, `danger`, `info`, `violet`, `neutral` (+ versi `Light`): makna semantik callout dan tabel lakukan/hindari.
- `ink`, `muted`, `line`, `zebra`, `codeBg`: teks dan permukaan.
- `series[0..4]`: warna diagram/kartu berurutan, semuanya lolos kontras dengan teks putih.

**Proporsi 60–30–10**: ±60% putih/kertas, ±30% warna primer (sampul, pembuka, header, intisari),
±10% aksen. Aksen yang terlalu banyak kehilangan fungsi sorotnya.

**Kontras** (WCAG 2.x) diperiksa `scripts/check_contrast.py`: teks isi ≥ 7:1, teks kecil ≥ 4,5:1,
teks besar/tebal di atas warna gelap ≥ 3:1. Jangan menyampaikan makna hanya lewat warna —
tabel lakukan/hindari juga diberi simbol ✓/✗, callout diberi label teks dan ikon.

**Cetak**: halaman isi berlatar putih; warna blok penuh hanya di sampul dan halaman pembuka agar hemat tinta.
Latar callout memakai versi `Light` yang tetap terbaca bila dicetak hitam-putih.

## 3. Tata letak

- **Margin** A4: 18 mm atas/samping, 20 mm bawah (ruang footer). B5/A5 mengecil proporsional.
- **Footer berjalan**: kiri judul buku atau "Modul N · judul pendek", kanan nomor halaman tebal
  berwarna primer — pembaca selalu tahu posisinya.
- **Sampul & pembuka bagian** memakai gradasi primer gelap→primer→primer2, motif dekoratif
  bertransparansi rendah, dan satu elemen aksen besar (nomor/ilustrasi). Pembuka bagian adalah "jeda napas"
  sekaligus peta: tujuan + daftar template/isi.
- **Ruang putih** dipakai sebagai pemisah, bukan garis. Jarak sebelum H2 ± 1,25 em, sesudah ± 0,55 em
  (judul menempel ke isinya — prinsip kedekatan).
- **Anti-terbelah**: diagram, callout, dan baris tabel tidak dipecah halaman; judul tidak ditinggal
  sendirian di dasar halaman; header tabel diulang.

## 4. Pola yang membuat buku *engaging*

1. **Janji di awal**: pembuka bagian menampilkan tujuan dan "yang akan Anda dapat" (template).
2. **Kicker** kecil di atas judul memberi konteks ("BAGIAN AWAL", "LAMPIRAN B").
3. **Lencana nomor** pada subjudul (`## 1. ...`) memberi rasa kemajuan.
4. **Kartu angka** (`:::stats`) untuk fakta kunci di halaman pengantar.
5. **Sebelum vs sesudah** membuat manfaat terlihat konkret.
6. **Template siap salin** mengubah bacaan menjadi alat kerja.
7. **Intisari + satu kalimat kunci** di akhir bab untuk retensi.
8. **Ritme**: teks → visual → teks. Setiap halaman isi idealnya punya satu jangkar visual.

## 5. Menulis untuk tata letak

- Paragraf 2–5 kalimat; > 7 baris A4 → pecah.
- Judul subbab berupa frasa bermakna ("Mengapa AI butuh kemudi?"), bukan label kosong ("Penjelasan").
- Butir daftar paralel secara tata bahasa (semua diawali kata kerja, atau semua frasa benda).
- Tabel: judul kolom singkat, isi sel ≤ ±25 kata; bila lebih, pertimbangkan subbab.
- Tebalkan maksimal satu frasa kunci per paragraf; tebal yang terlalu banyak = tidak ada yang menonjol.
- Istilah asing dimiringkan saat pertama muncul dan diberi padanan.
- Konsisten: satu istilah untuk satu konsep di seluruh buku (misalnya "murid" atau "siswa", pilih satu).

## 6. DOCX vs PDF

PDF adalah versi referensi (tata letak presisi). DOCX dirancang **setara secara visual** dan mudah disunting:
sampul & gambar berupa gambar, pembuka bagian berupa tabel berwarna dengan judul Heading 1 (masuk daftar isi),
callout berupa tabel satu sel dengan garis kiri berwarna, template berupa tabel dua baris.
Pemenggalan halaman DOCX ditentukan Word, sehingga jumlah halaman bisa sedikit berbeda dari PDF.
