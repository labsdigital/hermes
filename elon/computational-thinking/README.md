# Computational Thinking — Modul Belajar Interaktif

Aplikasi pembelajaran interaktif **Computational Thinking** (Berpikir Komputasional) dalam satu file HTML, menggunakan tema **"Modern Split-Pane Desktop"** (referensi: https://taraka.id/AGENTS/ui.txt).

**Demo:** buka `index.html` langsung di peramban — tanpa build step.

## Fitur

- **10 Slide Materi & Praktik**
  1. Pengenalan Computational Thinking
  2. Dekomposisi
  3. Pengenalan Pola
  4. Abstraksi
  5. Desain Algoritma
  6. Lab: Dekomposisi — klik untuk memecah masalah besar menjadi 20 bagian kecil
  7. Lab: Pola — temukan 4 kartu dengan susunan titik yang sama dengan pola target
  8. Lab: Abstraksi — kurasi data: pilih simpan/buang pada 2 skenario (8 data per skenario)
  9. Lab: Algoritma — susun 6 langkah menjadi urutan yang benar (2 tantangan)
  10. Kuis — 5 soal pilihan ganda, umpan balik instan + pembahasan, skor tersimpan

- **Navigasi**
  - Sidebar gelap (300px) dengan menu akordeon bergrup: Materi / Laboratorium / Evaluasi
  - Tombol FAB Prev / Next / Home di kanan bawah
  - Deep link via hash: `#slide-1` … `#slide-10`
  - Navigasi keyboard: panah kiri/kanan

- **Progres & Persistensi**
  - Progres disimpan di `localStorage` (slide selesai, status lab, skor kuis terbaik)
  - Indikator progres di sidebar dan window header
  - Tombol *Reset Progres* di footer sidebar

- **Responsif**: sidebar menjadi overlay + hamburger di layar < 768px

## Teknologi

| Bagian | Teknologi |
|---|---|
| Struktur & gaya | HTML5 + Tailwind CSS (CDN) |
| Ikon | Lucide (CDN) |
| Logika | Vanilla JavaScript (tanpa framework) |
| Font | Inter (Google Fonts) |

## Desain Sistem (Ringkas)

- Sidebar gelap `#18181b` / logo `#09090b`, workspace terang `#fafafa`
- Aksen utama oranye `#f97316`, sekunder teal `#14b8a6`
- Kartu `rounded-3xl`, border `#e4e4e7`, shadow `0 12px 30px -5px rgba(0,0,0,.05)`
- Heading 2-tone: hitam + kata kunci oranye
- Transisi slide `cubic-bezier(0.4, 0, 0.2, 1)` 400ms
