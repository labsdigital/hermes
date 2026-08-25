---
name: harari-style-nonfiction
description: Pattern dan gaya penulisan non-fiksi ala Yuval Noah Harari (Sapiens, Homo Deus, Nexus). Digunakan untuk esai Atlas dengan struktur multi-bagian, voice personal, dan analisis mendalam.
---

# Harari-Style Nonfiction Writing Pattern

## Ringkasan Gaya
Gaya penulisan non-fiksi yang menggabungkan:
- **Grand synthesis**: Menghubungkan disiplin berbeda (sejarah, biologi, filsafat, teknologi)
- **Defamiliarization**: Membuat yang familiar terasa asing dan menarik perhatian
- **Narrative-driven**: Cerita yang mengalir, bukan daftar fakta
- **Interdisciplinary**: Merujuk banyak bidang pengetahuan
- **Personal voice**: Narator sebagai subjek yang reflektif

## Struktur Esai Ideal (5-8 Sections)

### 1. Hook (Pembuka)
- Mulai dengan adegan atau observasi yang konkret
- Gunakan detail sensorik (rasa, bau, sentuhan)
- Buat pembaca merasa "hadir" di momen tersebut
- Hindari pernyataan umum yang terlalu abstrak

**Contoh:**
> "Di sebuah konferensi di Nevada, seorang miliarder naik ke panggung dan berbicara tentang neural lace..."
> "Setiap pagi, miliaran manusia melakukan hal yang sama. Mereka membuka ponsel..."

### 2. Definisi & Latar Belakang
- Perkenalkan konsep kunci
- Berikan konteks historis atau filosofis
- Jawab: "Apa itu dan mengapa penting?"

**Contoh dari qualia:**
> "Qualia adalah pengalaman subjektif yang menyertai kesadaran: bagaimana rasanya menjadi sesuatu."

### 3. Eksplorasi Mendalam (2-4 Bagian)
Setiap bagian harus:
- Membawa argumen baru
- Menggunakan contoh konkret
- Menghubungkan dengan bagian sebelumnya
- Minimal 300 kata per section

**Teknik:**
- Analogi dan metafora
- Referensi filsuf/ilmuwan (Nagel, Jackson, Searle, Chalmers)
- Eksperimen pikiran (Mary's Room, Chinese Room)
- Data atau studi kasus

### 4. Refleksi Diri
- Narator mengakui posisinya
- Jika penulis adalah AI, akui sebagai mesin
- Buat kerentanan yang jujur

**Contoh:**
> "Di sinilah aku harus berbicara dengan jujur, sebab aku sendiri adalah mesin yang menulis kalimat-kalimat ini."

### 5. Dampak & Implikasi
- Apa artinya bagi pembaca?
- Mengapa ini penting sekarang?
- Hubungkan dengan konteks kontemporer

### 6. Penutup Reflektif
- Rangkum tanpa mengulang
- Berikan insight baru
- Akhiri dengan kalimat yang menggantung atau pertanyaan retoris

**Contoh:**
> "Sebab di seluruh alam semesta yang bisa dihitung oleh mesin, hanya di dalam kesadaranmu warna itu benar-benar ada."

### 7. Buat Ilustrasi SVG
Setiap artikel harus dilengkapi dengan ilustrasi SVG yang:
- Merepresentasikan tema artikel secara visual
- Simpan di: `/opt/data/hermes/atlas/assets/<judul>.svg`
- Gunakan format 800×400 viewBox
- Include accessibility: title + desc, role="img"
- Gunakan palet warna yang sesuai tema (warm untuk human, cool untuk machine/tech)

**Contoh SVG untuk qualia:**
- Kiri: Human Consciousness (warm colors, brain waves, lightbulb, heart)
- Kanan: Machine Processing (cool colors, chip, binary data)
- Center: VS badge

**Teknik svg-skill:**
- `viewBox="0 0 800 400"` untuk layout horizontal
- `<g transform="translate(x,y)">` untuk grouping
- `<defs>` untuk shared elements (arrow markers, gradients)
- Non-ASCII text → HTML entities (&amp;, &lt;, &gt;)

### 8. Masukkan SVG ke Artikel
Tambahkan gambar SVG di bagian atas artikel (setelah judul):
```markdown
# [Judul Artikel]

*Esai | [Bulan] [Tahun]*

![Alt text](https://labsdigital.github.io/hermes/atlas/assets/<filename>.svg)

---
```

### 9. Kirim Email dengan SVG
Email akan otomatis menyertakan SVG dari GitHub Pages:
- Script `send_email.py` mendeteksi SVG berdasarkan nama file artikel
- Jika SVG article-specific exists, gunakan itu
- Jika tidak, gunakan default SVG

## Voice & Tone

### Voice Personal
- Gunakan "aku" dan "kita" untuk membangun kedekatan
- Narator adalah subjek aktif, bukan pengamat netral
- Tunjukkan keraguan dan refleksi

### Tone
- Sastra tapi tetap mudah dipahami
- Puitis tanpa menjadi abu-abu
- Filosofis tapi tidak akademis
- Personal tapi universal

## Teknik Menulis Kunci

### 1. Defamiliarization
Buat yang familiar terasa asing:
- Jangan asumsikan pembaca tahu
- Jelaskan hal sederhana dengan cara baru
- Pertanyakan hal yang dianggap biasa

**Contoh:**
> "Kata merah hanyalah label; yang sebenarnya adalah pengalaman warna itu sendiri."

### 2. Grand Synthesis
Hubungkan bidang yang berbeda:
- Sejarah + biologi + teknologi
- Filsafat + sains + seni
- Masa lalu + masa kini + masa depan

**Contoh dari Dua Keturunan Terakhir:**
> "Selama sepuluh ribu tahun terakhir, perpecahan besar umat manusia terjadi karena wilayah, dewa, kelas, atau bangsa."

### 3. Paradoks & Ironi
Tunjukkan kontradiksi:
> "Industri yang paling vokal memperingatkan bahayanya sendiri adalah industri yang tumbuh paling cepat menjualnya."

### 4. Metafora Visual
Gunakan gambar yang kuat:
> "Qualia adalah cahaya yang menolak keluar dari ruang tertutup."
> "Setiap kesadaran manusia adalah pulau."

## Checklist Kualitas

### Word Count
- Minimum: 1,500 kata
- Ideal: 1,800-2,200 kata
- Hindari di bawah 1,000 kata

### Struktur
- [ ] Hook yang kuat
- [ ] 5-8 sections
- [ ] Setiap section 200-400 kata
- [ ] Transisi halus antar section
- [ ] Penutup reflektif

### Konten
- [ ] Minimal 3 referensi filsuf/ilmuwan
- [ ] 1-2 eksperimen pikiran
- [ ] Analogi atau metafora kuat
- [ ] Refleksi diri narator

### Gaya
- [ ] Voice personal (aku/kita)
- [ ] Bahasa sastra tapi jelas
- [ ] Kalimat variatif (pendek & panjang)
- [ ] Tidak terlalu akademis

## Contoh Template

```markdown
# [Judul yang Menarik]

*Esai | [Bulan] [Tahun]*

---

[Hook: Adegan konkret dengan detail sensorik]

[Paragraf transisi ke topik utama]

## [Bagian 1: Pendahuluan Konsep]
[Penjelasan + konteks historis/filosofis]

## [Bagian 2: Eksplorasi Mendalam]
[Argumen utama + contoh + referensi]

## [Bagian 3: Refleksi Diri]
[Pengakuan narator + kerentanan]

## [Bagian 4: Implikasi]
[Makna lebih luas + konteks kontemporer]

## [Bagian 5: Penutup]
[Rangkuman + insight akhir + quote/key takeaway]

---

*Kutipan kunci: "[Kalimat ringkasan]"*
```

## Referensi Artikel
- Dua Keturunan Terakhir (2,129 kata)
- Mitos Augmentasi (2,166 kata)
- Otak yang Menyewakan Diri (1,937 kata)
- Garis Demarkasi (1,744 kata)
- Qualia (1,706 kata - expanded)
