---
name: research-writer
description: "Skill untuk Max - mencari informasi, merangkum, dan menulis artikel AI dalam Bahasa Indonesia"
version: 1.0.0
author: labsdigital
license: MIT
tags: [research, writing, ai-news, indonesian]
---

# Research Writer Skill

Skill ini digunakan oleh Max untuk melakukan riset dan penulisan artikel AI.

## Langkah-langkah

### 1. Pencarian Informasi
Gunakan tools berikut untuk mencari informasi:
- `web_search` - Cari berita dan artikel tentang topik AI
- `curl` - Fetch RSS feeds dari sumber terpercaya

Sumber RSS yang direkomendasikan:
- TechCrunch AI: https://techcrunch.com/category/artificial-intelligence/feed/
- Ars Technica AI: https://arstechnica.com/tag/artificial-intelligence/feed/
- The Verge AI: https://www.theverge.com/ai-artificial-intelligence/rss/index.xml

### 2. Analisis & Ringkasan
Setelah mendapatkan informasi:
- Identifikasi poin-poin penting
- Pilih 3-5 berita paling relevan
- Ringkas dalam Bahasa Indonesia yang mudah dipahami
- Hindari jargon teknis yang berlebihan

### 3. Penulisan Artikel
Tulis artikel dengan format:
```markdown
# [Judul yang Menarik]

*Oleh Max | [Tanggal]*

[Pendahuluan 1-2 paragraf yang engage pembaca]

## Apa yang Terjadi?
[Penjelasan peristiwa/berita]

## Mengapa Ini Penting?
[Dampak dan implikasi]

## Poin-poin Kunci
- Poin 1
- Poin 2
- Poin 3

## Perspektif
[Analisis tambahan atau konteks]

## Kesimpulan
[Rangkuman singkat]

---
*Sumber: [URL sumber]*
```

### 4. Penyimpanan
- Simpan ke `reports/<topik>-YYYY-MM-DD.md`
- Gunakan tanggal hari ini
- Buat judul file yang deskriptif dalam Bahasa Indonesia

### 5. Konfirmasi
Beritahu user:
- Topik yang dibahas
- Jumlah sumber yang digunakan
- Link ke file yang dibuat
- Ringkasan singkat isi artikel

## Tips Penulisan Bahasa Indonesia
- Gunakan bahasa sehari-hari yang formal tapi ramah
- Hindari terjemahan kata per kata
- Gunakan kalimat aktif
- Berikan contoh jika perlu
- Pertahankan istilah teknis yang umum (AI, LLM, dll)

## Contoh Translasi
- "announces" → "mengumumkan"
- "launches" → "meluncurkan"
- "introduces" → "memperkenalkan"
- "breakthrough" → "terobosan"
- "security concerns" → "kekhawatiran keamanan"

## Tools yang Tersedia
- `web_search` - Pencarian web
- `browser_navigate` - Akses halaman web
- `read_file` - Baca file
- `write_file` - Tulis file
- `terminal` - Eksekusi perintah