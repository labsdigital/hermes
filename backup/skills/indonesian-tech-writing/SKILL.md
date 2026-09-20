---
name: indonesian-tech-writing
description: "Write technical content in natural Indonesian language."
version: 1.1.0
author: Hermes Agent + labsdigital
license: MIT
tags: [indonesian, translation, tech-writing]
---

# Indonesian Tech Writing

Panduan menulis konten teknologi dalam Bahasa Indonesia natural.

## Style Guide
- Kalimat aktif
- Paragraf pendek
- Istilah teknis tetap Inggris jika umum

## Translation Dictionary
- announces → mengumumkan
- launches → meluncurkan
- improves → meningkatkan

## Example
**Before:** "OpenAI announced the release of a new model"
**After:** "OpenAI merilis model terbaru"

## Content Pattern

```markdown
# [Judul]

*Oleh [Nama] | Tanggal: YYYY-MM-DD*

## Poin Penting
- Poin 1
- Poin 2

## Kesimpulan
```

## Article Arc (artikel panjang 1200+ kata)

Untuk artikel riset/opini yang lebih panjang, gunakan arc naratif 7 bagian —
teruji di artikel experiential-learning-virtual-manipulative (2026-08-23):

1. **Hook** — buka dengan skenario konkret seorang guru/pembaca (nama fiktif,
   situasi nyata), lalu satu data pembanding yang mengagetkan. Tutup dengan
   pertanyaan kunci artikel.
2. **Konteks** — definisikan 2–3 konsep inti, masing-masing dengan sub-heading
   `###`. Istilah teknis dibold saat pertama kali diperkenalkan.
3. **Solusi** — gabungkan konsep-konsep tadi; tabel markdown untuk memetakan
   teori ke aktivitas konkret sangat efektif di bagian ini.
4. **Implementasi** — studi kasus nyata yang sudah ada (repo/artikel/alat),
   langkah demi langkah, lengkap dengan contoh alur berwaktu (mis. "Menit 0–5").
5. **Challenges** — format "**Tantangan.** Solusinya: ..." per poin.
6. **Future** — tren + peran pembaca di masa depan; akhiri dengan kalimat
   penguatan ("peran guru tidak berkurang—ia bergeser").
7. **Call to Action** — langkah bernomor yang bisa dieksekusi minggu ini,
   ditutup satu kalimat kuat.

## Verifikasi Sumber (wajib untuk klaim riset)

- Setiap angka/kutipan diverifikasi ke sumber primer sebelum masuk draft:
  Crossref (`api.crossref.org/works?query.bibliographic=...`) untuk keberadaan
  paper + DOI, OpenAlex (`api.openalex.org/works/doi:<DOI>`) untuk abstrak +
  jumlah sitasi. Detail ladder + fallback: `references/riset-verifikasi.md`.
- Cantumkan sumber bernomor di akhir artikel (*Sumber:* dengan DOI/URL).
- Angka spesifik (effect size, skor) yang GAGAL diverifikasi → parafrase
  kualitatif dengan sitasi DOI, jangan tulis angka dari ingatan.
- PDF laporan institusi (contoh: country note OECD) bisa berupa shell website
  tanpa isi — verifikasi angka lewat tabel Wikipedia atau sumber data lain.

## Mistakes to Avoid
1. Over-translation
2. Literal translation
3. Stiff formality
4. Listing without explaining - Don't just list concepts, connect them to reader's experience
5. Forgetting the hook - Always open with something relatable (a teacher's struggle, a common frustration)
6. **Race condition on shared file writes** - When writing to a file path that other agents may also write (e.g. `reports/<name>.md` in a shared subagent repo), `patch` may fail if the file was modified by another agent since your last read. Always `read_file` immediately before `write_file`; if the file was modified, use `write_file` (full overwrite) not `patch`.
7. **Title overuse of 'ketika'** - Avoid using 'ketika' in article titles as it's overused. Use alternatives like 'di tengah', 'di saat', 'saat', or restructure the title entirely.

## Advanced: Analogical Frameworks for Research/Opinion Articles
For opinion/research articles, use psychological or everyday analogies to explain complex AI concepts:
- **Parenting styles (Baumrind)**: Authoritative vs Authoritarian for AI safety/trust
- **Child development (Piaget)**: Staged learning for AI curriculum design
- **School system**: Grade progression (TK→SD→SMP→SMA→Kuliah) for training data ordering
- **Obedience vs understanding**: RLHF pitfalls as "performative goodness" vs genuine comprehension
- **Teacher-student dynamics**: Learn-by-teaching vs learn-by-being-tutored cognitive load differences

These frameworks make technical content accessible to general Indonesian readers while maintaining analytical depth.

## Related Skills
- `humanizer`
- `github-push-workflow`

Pipeline konkret publikasi artikel Max (lokasi repo sebenarnya di
`/opt/data/hermes` yang berupa nested git repo, urutan commit/push, script
sync Airtable + idempotensi): lihat `references/publikasi-pipeline.md`.