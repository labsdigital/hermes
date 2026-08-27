# Bab 14: Komodifikasi Perhatian (Hiper-Silo)

*Esai Non-Fiksi | Agustus 2026*

---

## Penjara Kehendak Sendiri

Algoritma rekomendasi tidak ingin memberimu apa yang kamu butuhkan. Mereka ingin membuatmu tetap menonton.

Setiap platform digital—YouTube, TikTok, Instagram, Facebook—menggunakan AI untuk memaksimalkan "engagement." Dan engagement diukur dengan satu metrik: waktu yang kamu habiskan di platform tersebut.

Hasilnya? Kamu terjebak dalam ruang gema (echo chamber) di mana kamu hanya melihat konten yang memperkuat keyakinanmu, memuaskan hasratmu, dan membuatmu terus scrolling.

Ini bukan kebetulan. Ini adalah desain.

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" aria-labelledby="silos-title">
  <title id="silos-title">Hiper-Silo: Penjara Algoritma Rekomendasi</title>
  
  <rect width="800" height="450" fill="#f8fafc"/>
  
  <!-- Title -->
  <text x="400" y="40" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#1e293b" font-weight="bold">Hiper-Silo</text>
  
  <!-- User in center -->
  <g transform="translate(400, 225)">
    <circle cx="0" cy="0" r="50" fill="#fef3c7" stroke="#f59e0b" stroke-width="3"/>
    <text x="0" y="5" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#78350f" font-weight="bold">Anda</text>
  </g>
  
  <!-- Silos around user -->
  <g transform="translate(400, 225)">
    <!-- Silo 1: Political echo chamber -->
    <rect x="-350" y="-200" width="150" height="100" rx="12" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
    <text x="-275" y="-175" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#1e40af" font-weight="bold">Politik</text>
    <text x="-275" y="-155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#64748b">Hanya sudut pandang A</text>
    <path d="M -200 -150 Q -100 -100 0 -50" stroke="#94a3b8" stroke-width="1" fill="none" stroke-dasharray="4,4"/>
    
    <!-- Silo 2: Consumerism -->
    <rect x="200" y="-200" width="150" height="100" rx="12" fill="#fce7f3" stroke="#ec4899" stroke-width="2"/>
    <text x="275" y="-175" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#9d174d" font-weight="bold">Konsumerisme</text>
    <text x="275" y="-155" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#64748b">Selalu ada yang harus dibeli</text>
    <path d="M 200 -150 Q 100 -100 0 -50" stroke="#94a3b8" stroke-width="1" fill="none" stroke-dasharray="4,4"/>
    
    <!-- Silo 3: Sensationalism -->
    <rect x="-350" y="100" width="150" height="100" rx="12" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
    <text x=" -275" y="125" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#14532d" font-weight="bold">Sensasionalisme</text>
    <text x="-275" y="145" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#64748b">Konten provokatif</text>
    <path d="M -200 150 Q -100 100 0 50" stroke="#94a3b8" stroke-width="1" fill="none" stroke-dasharray="4,4"/>
    
    <!-- Silo 4: Conspiracy -->
    <rect x="200" y="100" width="150" height="100" rx="12" fill="#fef2f2" stroke="#ef4444" stroke-width="2"/>
    <text x="275" y="125" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#dc2626" font-weight="bold">Konspirasi</text>
    <text x="275" y="145" text-anchor="middle" font-family="sans-serif" font-size="10" fill="#64748b">Teori tanpa bukti</text>
    <path d="M 200 150 Q 100 100 0 50" stroke="#94a3b8" stroke-width="1" fill="none" stroke-dasharray="4,4"/>
  </g>
  
  <!-- Algorithm at top -->
  <g transform="translate(400, 80)">
    <rect x="0" y="0" width="200" height="60" rx="10" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>
    <text x="100" y="25" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#334155" font-weight="bold">Algoritma Rekomendasi</text>
    <text x="100" y="45" text-anchor="middle" font-family="sans-serif" font-size="11" fill="#64748b">Tujuan: Maximize Engagement</text>
  </g>
  
  <!-- Connection from algorithm to silos -->
  <path d="M 400 140 Q 400 180 350 200" stroke="#94a3b8" stroke-width="2" fill="none" marker-end="url(#arrowGray)"/>
  <path d="M 400 140 Q 400 180 450 200" stroke="#94a3b8" stroke-width="2" fill="none" marker-end="url(#arrowGray)"/>
  
  <!-- Warning -->
  <g transform="translate(100, 400)">
    <rect x="0" y="0" width="600" height="40" rx="8" fill="#fef2f2" stroke="#fecaca" stroke-width="1"/>
    <text x="300" y="26" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#991b1b">Risiko: Terjebak dalam Bubble—tidak pernah melihat perspektif lain</text>
  </g>
  
  <defs>
    <marker id="arrowGray" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto">
      <path d="M0,0 L10,3 L0,6 Z" fill="#94a3b8"/>
    </marker>
  </defs>
</svg>
```

## The Attention Economy

Ekonomi perhatian (attention economy) adalah model bisnis di mana perhatian manusia adalah komoditas. Platform digital bersaing untuk mendapatkan dan mempertahankan perhatian pengguna, karena perhatian tersebut dapat dijual kepada pengiklan.

AI menjadi senjata utama dalam perang ini. Algoritma rekomendasi mempelajari preferensi setiap pengguna dan menyajikan konten yang paling mungkin membuat mereka tetap scrolling.

Hasilnya? Kita semua terjebak dalam "filter bubbles"—dunia kecil di mana hanya informasi yang kita setujui yang kita lihat.

## The Fragmentation of Reality

Ketika setiap orang hidup dalam bubble mereka sendiri, tidak ada lagi realitas bersama. Tidak ada lagi fakta dasar yang disepakati bersama.

Ini merusak demokrasi. Demokrasi membutuhkan warga yang berbagi informasi dasar yang sama, agar bisa berdebat tentang kebijakan dan nilai. Tanpa shared reality, debat menjadi mustahil—yang tersisa hanyalah pertempuran antara truth claims yang saling bertentangan.

## The Psychology of Addiction

Algoritma rekomendasi memanfaatkan psikologi manusia untuk membuat ketagihan. Prinsip-prinsip yang digunakan termasuk:

- **Variable rewards**: Seperti mesin slot, konten muncul secara tidak terduga, melepaskan dopamine setiap kali ada sesuatu yang menarik.
- **Loss aversion**: Kita takut ketinggalan (FOMO—fear of missing out), sehingga terus memeriksa notifikasi.
- **Social proof**: Kita cenderung mengikuti apa yang dilakukan orang lain, sehingga konten viral menjadi semakin viral.

Ini bukan kebetulan. Ini adalah desain yang disengaja.

## Breaking Out of the Silo

Ada beberapa cara untuk melawan hiper-silo:

1. **Media literacy**: Belajar mengenali bias dalam konten dan memahami bagaimana algoritma bekerja.
2. **Diversifikasi sumber**: Sengaja mengonsumsi konten dari berbagai perspektif.
3. **Digital detox**: Mengurangi waktu di layar secara periodik.
4. **Support regulation**: Mendukung kebijakan yang menuntut transparansi algoritma.

Tantangannya adalah bahwa keluar dari bubble membutuhkan usaha—dan usaha adalah sesuatu yang algoritma lawan dengan menawarkan kemudahan.

## The Democratic Implications

Bagi demokrasi, hiper-silo adalah ancaman eksistensial. Tanpa dialog yang didasarkan pada fakta bersama, tidak ada konsensus yang mungkin. Tanpa konsensus, tidak ada tindakan kolektif.

Kita menghadapi pilihan: terus tenggelam dalam bubble-bubble terpisah, atau berusaha membangun jembatan kembali ke realitas bersama.

Pilihan itu menentukan masa depan masyarakat kita.

---

*Kutipan kunci: "Platform tidak menjual produk kepada Anda. Mereka menjual perhatian Anda kepada pengiklan. Dan mereka menggunakan AI untuk memastikan perhatian itu tidak pernah berhenti."*
