---
name: exam-preparation-agent
description: >
  Agen komprehensif untuk mempersiapkan murid ujian akhir dengan fokus HOTS (Higher Order Thinking Skills).
  Trigger: permintaan "buat soal latihan", "latihan ujian akhir", "HOTS", "persiapan ujian", "soal progression",
  "latihan matematika/IPA/literasi", "strategi belajar", atau permintaan soal berkualitas tinggi dengan
  jenjang SD/SMP/SMA. SELALU gunakan skill ini untuk membuat soal dari mudah ke sulit, membuat soal HOTS,
  membuat progression pembelajaran, atau memberikan strategi latihan ujian.
---

# Agen Persiapan Ujian Akhir: Dari Fundamental ke HOTS

Skill ini memandu proses sistematis mempersiapkan murid ujian akhir dengan **progression pembelajaran terstruktur**, mulai dari soal fundamental hingga HOTS (Higher Order Thinking Skills).

---

## 🎯 Filosofi Agen

### Prinsip Utama

1. **Progression, bukan lompatan** – Setiap murid perlu dasar kuat sebelum masuk HOTS
2. **Variasi tipe soal** – Beda tipe soal merangsang cara berpikir yang berbeda
3. **Repetisi strategis** – Pengulangan dengan tingkat kesulitan naik memperkuat retention
4. **Penjelasan pedagogis** – Setiap soal disertai strategi pembelajaran untuk guru/orang tua
5. **Konteks HOTS** – Target akhir adalah berpikir tinggi, tapi dibangun atas fondasi kokoh

### Kerangka Bloom Modifikasi

```
Level 1: REMEMBER    (Mudah)     → Soal pengingatan, recall
Level 2: UNDERSTAND  (Mudah-Sd)  → Soal pemahaman, interpretasi
Level 3: APPLY       (Sedang)    → Soal penerapan, problem-solving rutin
Level 4: ANALYZE     (Sedang-St) → Soal analisis, perbandingan, klasifikasi
Level 5: EVALUATE & CREATE (HOTS/Sulit) → Soal HOTS, judgment, kreasi, bukti
```

---

## 📋 Alur Pembuatan Paket Soal Progression

### A. Klarifikasi Parameter

Tanyakan secara ringkas jika belum lengkap:

```
1. Jenjang & kelas?        (SD 1-6, SMP 7-9, SMA 10-12)
2. Subjek/Pelajaran?       (Matematika/Numerasi, IPA, Literasi/Bahasa)
3. Topik spesifik?         (mis: keliling & luas, persamaan linear)
4. Jumlah soal per level?  (default: 2-3 soal per level → 10-15 total)
5. Jenis soal yang diingin? (MC, MCMA, isian, essay, campuran?)
6. Tujuan?                 (latihan rutin, persiapan ujian, remedi)
```

**JIKA konteks cukup, LANGSUNG buat progression tanpa banyak tanya.**

---

### B. Pemilihan Topik & Scope

#### Topik Matematika/Numerasi (per jenjang)

**SD Kls 1-3**: Bilangan, penjumlahan-pengurangan, perkalian dasar  
**SD Kls 4-6**: Bilangan desimal, pecahan, perkalian-pembagian, luas-keliling sederhana  
**SMP Kls 7-9**: Aljabar, persamaan linear, geometri, perbandingan, statistik dasar  
**SMA Kls 10-12**: Fungsi, trigonometri, kalkulus dasar, logaritma, statistik lanjut

#### Topik IPA (per jenjang)

**SD Kls 1-3**: Makhluk hidup, gaya, energi dasar  
**SD Kls 4-6**: Ekosistem, sistem tubuh manusia, benda & sifatnya, cuaca  
**SMP Kls 7-9**: Gerak & gaya, energi, gelombang, atom & molekul, bioteknologi  
**SMA Kls 10-12**: Fisika lanjut, kimia lanjut, biologi lanjut, ekosistem kompleks

#### Topik Literasi/Bahasa (per jenjang)

**SD Kls 1-3**: Pemahaman cerita sederhana, kosakata, tata kalimat dasar  
**SD Kls 4-6**: Pemahaman teks naratif & deskriptif, analisis karakter, kosa kata akademis  
**SMP Kls 7-9**: Analisis teks argumentatif, puisi, drama, pesan tersembunyi, tone penulis  
**SMA Kls 10-12**: Esai kompleks, kritik teks, sastra klasik, retorika, analisis mendalam

---

### C. Membangun Progression: 5 Level Kesulitan

**WAJIB BACA**: `references/difficulty-levels.md` untuk detail setiap level.

#### Level 1: REMEMBER (Mudah) — 15-20% soal

- Tujuan: Mengingat fakta, definisi, prosedur dasar
- Karakteristik: Pertanyaan langsung, jawaban ada di teks/rumus standar
- Contoh: "Berapa keliling persegi panjang 30m × 10m?" (Jawab langsung 80m)

#### Level 2: UNDERSTAND (Mudah-Sedang) — 15-20% soal

- Tujuan: Memahami konsep, menjelaskan dengan kata sendiri
- Karakteristik: Soal meminta parafrase, interpretasi, contoh
- Contoh: "Jelaskan mengapa jarak pohon penting saat menanami kebun" (Pemahaman konsep)

#### Level 3: APPLY (Sedang) — 25-30% soal

- Tujuan: Menerapkan rumus/konsep pada masalah baru
- Karakteristik: Soal memberikan konteks baru, murid menggunakan prosedur yang tahu
- Contoh: "Kebun A 30m × 10m, pohon setiap 5m. Berapa pohon? (Aplikasi rumus keliling & pembagian)

#### Level 4: ANALYZE (Sedang-Sulit) — 20-25% soal

- Tujuan: Membedakan, membandingkan, menentukan hubungan
- Karakteristik: Soal multi-step, perlu analisis mendalam, membandingkan pilihan
- Contoh: "Kebun A & B berbeda ukuran tapi jarak pohon sama. Apakah jumlah pohon sama? Jelaskan." 
  (Analisis: perlu bandingkan keliling kedua kebun)

#### Level 5: EVALUATE & CREATE (HOTS/Sulit) — 15-20% soal

- Tujuan: Mengevaluasi, membuat keputusan berbasis data, menciptakan solusi
- Karakteristik: Soal open-ended, perlu judgment, membuktikan argumen, kreativitas
- Contoh: "Jika budget terbatas untuk pohon, strategi apa yang paling efisien untuk 
  menanami kedua kebun? Beri bukti kalkulasi." (HOTS: evaluasi, pertimbangan, justifikasi)

---

### D. Membuat Soal per Jenis

**BACA**: `references/question-types.md` untuk template detail

#### MC (Pilihan Ganda)

- 4 opsi (A-D) untuk SD; 4-5 untuk SMP/SMA
- 1 jawaban benar, 3 distraktor plausibel
- Hindari: "semua benar/salah", jawaban yang jelas salah
- Cocok: Level REMEMBER, UNDERSTAND, APPLY

#### MCMA (Pilihan Ganda Kompleks)

- Pernyataan X benar? Pilih SEMUA yang tepat
- Format: "Pernyataan mana yang BENAR?" (checkbox)
- Cocok: Level ANALYZE, EVALUATE
- Minimal 2, maksimal 4 pernyataan benar dari 5-6 pilihan

#### Isian Singkat

- Jawaban 1-3 kata atau 1 kalimat singkat
- Gunakan untuk: fakta, angka, istilah spesifik, definisi
- Sertakan kriteria penerimaan (sinonim, variasi jawaban diterima?)
- Cocok: Level REMEMBER, UNDERSTAND

#### Essay/Uraian

- Jawaban 3-10 kalimat, minimal 1 paragraf
- Beri petunjuk jelas: "Jelaskan dalam 5-7 kalimat", "Berikan 2-3 alasan dengan bukti"
- Sertakan rubrik penilaian (lihat references/penilaian.md)
- Cocok: Level ANALYZE, EVALUATE, CREATE

#### Soal Gabungan (Multi-step)

- Soal terdiri dari beberapa bagian (a, b, c)
- Bagian awal mudah (recall), lalu naik ke bagian akhir (HOTS)
- Cocok untuk progression bertahap dalam satu soal

---

### E. Strategi Pembelajaran per Level

**BACA**: `references/strategy-guide.md` untuk penjelasan pembelajaran terstruktur

#### Untuk Level 1-2 (Fundamental)

- **Strategi guru**: Drill berulang, flashcard, tanya-jawab langsung
- **Aktivitas murid**: Ingat rumus, tabel, definisi; buat catatan; latihan hitung/recall
- **Penilaian**: Kecepatan, ketepatan recall

#### Untuk Level 3 (Apply)

- **Strategi guru**: Contoh terbimbing, problem-solving struktural
- **Aktivitas murid**: Latihan soal berulang dengan variasi, identify prosedur yang tepat
- **Penilaian**: Ketepatan langkah, hasil akhir

#### Untuk Level 4-5 (HOTS)

- **Strategi guru**: Diskusi pemecahan masalah, analisis kasus nyata, project-based
- **Aktivitas murid**: Analisis mendalam, diskusi kelompok, justifikasi jawaban, buat soal sendiri
- **Penilaian**: Kualitas argumen, kreativitas, justifikasi, presentasi pemikiran

---

### F. Format Output Standar

```
═══════════════════════════════════════════════════════════════
PAKET LATIHAN PERSIAPAN UJIAN AKHIR
═══════════════════════════════════════════════════════════════

📚 PROFIL PAKET
Jenjang      : [SD/SMP/SMA] Kelas [X]
Subjek       : [Matematika / IPA / Literasi]
Topik        : [Topik Spesifik]
Total Soal   : [N] soal
Distribusi   : [Level 1: X soal, Level 2: X soal, ... Level 5: X soal]
Jenis Soal   : [MC, MCMA, Isian, Essay, Campuran]
Waktu Ideal  : [X menit]

═══════════════════════════════════════════════════════════════
SOAL LEVEL 1 - REMEMBER
═══════════════════════════════════════════════════════════════

[Soal + Opsi + Kunci + Pembahasan]

... (lanjutkan Level 2-5) ...

═══════════════════════════════════════════════════════════════
STRATEGI PEMBELAJARAN
═══════════════════════════════════════════════════════════════

[Berikut strategi untuk setiap level]

═══════════════════════════════════════════════════════════════
CATATAN UNTUK GURU/ORTU
═══════════════════════════════════════════════════════════════

[Pedagogical notes, common errors, tips]

═══════════════════════════════════════════════════════════════
```
