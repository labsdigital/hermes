# Bab 17: Beban Lingkungan Ekstrem

*Esai Non-Fiksi | Agustus 2026*

---

## Harga Tersembunyi dari Kecerdasan Buatan

Data center AI membutuhkan energi luar biasa.

Setiap kali seseorang menanyakan sesuatu kepada AI, prosesnya melibatkan jutaan operasi komputasi—embedding, attention mechanisms, matrix multiplications—yang semuanya membutuhkan listrik. Dan listrik ini, sebagian besar masih berasal dari sumber fosil.

Bayangkan ini: satu pertanyaan kepada ChatGPT mengonsumsi energi setara dengan menyalakan lampu LED selama beberapa menit. Sekarang bayangkan miliaran pertanyaan per hari.

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 450" role="img" aria-labelledby="environment-title">
  <title id="environment-title">Beban Lingkungan Ekstrem dari AI</title>
  
  <rect width="800" height="450" fill="#f8fafc"/>
  
  <!-- Title -->
  <text x="400" y="40" text-anchor="middle" font-family="Georgia, serif" font-size="22" fill="#1e293b" font-weight="bold">Beban Lingkungan Ekstrem</text>
  
  <!-- Energy consumption comparison -->
  <g transform="translate(50, 80)">
    <text x="150" y="20" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#14532d" font-weight="bold">Konsumsi Energi per Query</text>
    
    <!-- Comparison bars -->
    <rect x="30" y="50" width="240" height="40" rx="6" fill="#dcfce7" stroke="#22c55e" stroke-width="1"/>
    <text x="50" y="75" font-family="sans-serif" font-size="13" fill="#166534">Google Search: ~0.3 Wh</text>
    
    <rect x="30" y="110" width="240" height="40" rx="6" fill="#fef3c7" stroke="#f59e0b" stroke-width="1"/>
    <text x="50" y="135" font-family="sans-serif" font-size="13" fill="#78350f">Web Browsing: ~1.0 Wh</text>
    
    <rect x="30" y="170" width="240" height="40" rx="6" fill="#fed7aa" stroke="#f97316" stroke-width="1"/>
    <text x="50" y="195" font-family="sans-serif" font-size="13" fill="#c2410c">Streaming Video: ~3.0 Wh</text>
    
    <rect x="30" y="230" width="240" height="40" rx="6" fill="#fecaca" stroke="#ef4444" stroke-width="2"/>
    <text x="50" y="255" font-family="sans-serif" font-size="13" fill="#dc2626" font-weight="bold">AI Query: ~10-30 Wh</text>
  </g>
  
  <!-- Data center visualization -->
  <g transform="translate(400, 80)">
    <rect x="0" y="0" width="350" height="300" rx="16" fill="#fef2f2" stroke="#fecaca" stroke-width="2"/>
    <text x="175" y="40" text-anchor="middle" font-family="Georgia, serif" font-size="18" fill="#991b1b" font-weight="bold">Data Center AI</text>
    
    <!-- Servers -->
    <rect x="30" y="80" width="60" height="100" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
    <rect x="100" y="80" width="60" height="100" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
    <rect x="170" y="80" width="60" height="100" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
    <rect x="240" y="80" width="60" height="100" rx="4" fill="#e2e8f0" stroke="#94a3b8" stroke-width="1"/>
    
    <!-- Heat waves -->
    <path d="M 50 70 Q 60 60 70 70" stroke="#ef4444" stroke-width="2" fill="none" opacity="0.5"/>
    <path d="M 120 70 Q 130 60 140 70" stroke="#ef4444" stroke-width="2" fill="none" opacity="0.5"/>
    <path d="M 190 70 Q 200 60 210 70" stroke="#ef4444" stroke-width="2" fill="none" opacity="0.5"/>
    <path d="M 260 70 Q 270 60 280 70" stroke="#ef4444" stroke-width="2" fill="none" opacity="0.5"/>
    
    <!-- Stats -->
    <text x="175" y="220" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#475569">Energi: ~1-2 GW total</text>
    <text x="175" y="245" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#475569">Air pendingin: ~1.2 liter/query</text>
    <text x="175" y="270" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#dc2626">Carbon: ~250g CO₂/query</text>
  </g>
  
  <!-- Impact summary -->
  <g transform="translate(100, 400)">
    <rect x="0" y="0" width="600" height="40" rx="8" fill="#fff7ed" stroke="#fde68a" stroke-width="1"/>
    <text x="300" y="26" text-anchor="middle" font-family="Georgia, serif" font-size="15" fill="#78350f">Total emisi AI setara dengan industri penerbangan global jika tidak ada regulasi</text>
  </g>
</svg>
```

## The Carbon Footprint of Training

Pelatihan model AI besar membutuhkan energi yang luar biasa. Model GPT-3, misalnya, mengonsumsi sekitar 1,287 MWh energi selama pelatihan—setara dengan emisi 550 ton CO₂, atau perjalanan mobil rata-rata selama 1.4 juta mil.

Ini belum termasuk energi untuk inferensi—proses menggunakan model setelah dilatih. Setiap pertanyaan yang Anda ajukan kepada ChatGPT membutuhkan komputasi tambahan, yang semuanya dikonsumsi listrik.

## Water Consumption

Selain energi, data center juga membutuhkan air dalam jumlah besar untuk pendinginan. Satu studi memperkirakan bahwa AI membutuhkan sekitar 1.2 liter air untuk setiap query yang diproses.

Dengan miliaran query per hari, ini berarti konsumsi air yang signifikan—terutama di daerah-daerah yang sudah mengalami stress air.

## The Greenwashing Problem

Banyak perusahaan teknologi mengklaim bahwa mereka berkomitmen pada sustainability. Mereka berinvestasi dalam energi terbarukan, menawarkan carbon offset programs, dan berbicara tentang "green AI."

Tapi klaim-klaim ini seringkali berlebihan. Studi menunjukkan bahwa sebagian besar offset yang ditawarkan perusahaan teknologi memiliki effectiveness yang diragukan—mereka seringkali membiayai proyek-proyek yang tidak akan berbeda secara meaningful dari business-as-usual.

Selain itu, pertumbuhan AI yang eksponensial mengikis setiap savings yang dihasilkan oleh efisiensi energi. Ini adalah Jevons paradox: semakin efisien teknologi, semakin banyak kita menggunakannya, sehingga total konsumsi meningkat.

## The Equity Dimension

Beban lingkungan AI tidak dirasakan secara merata. Data center sering ditempatkan di daerah-daerah yang sudah marginal—di mana regulasi lingkungan lemah dan communities memiliki political power yang terbatas untuk menolak mereka.

Ini adalah bentuk environmental injustice lainnya: manfaat AI dinikmati oleh mereka yang mampu membayar, sementara biayanya dibayar oleh mereka yang paling rentan.

## Toward Sustainable AI

Beberapa langkah可以向更可持续的方向发展：

1. **Energy-efficient models**: Mengembangkan model yang lebih efisien dalam komputasi dan energi.
2. **Renewable energy commitment**: Komitmen nyata untuk menggunakan energi terbarukan, bukan sekadar offset.
3. **Right to repair**: Memungkinkan data center untuk repaired dan diupgrade, bukan diganti seluruhnya.
4. **Regulation**: Regulasi yang memaksa transparansi dalam konsumsi energi dan emisi.

Tapi tanpa perubahan sistemik, pertumbuhan AI yang saat ini terjadi akan terus memperburuk krisis iklim.

## The Paradox of Progress

Di sinilah paradoksnya: teknologi yang menjanjikan solusi untuk masalah manusia (kesehatan, pendidikan, efisiensi) justru memperburuk masalah terbesar umat manusia—perubahan iklim.

Pertanyaannya adalah apakah kita bisa menikmati benefits AI tanpa mengorbankan planet kita. Ataukah kita harus memilih—antara kemajuan teknologi dan kelangsungan hidup ekosistem?

---

*Kutipan kunci: "Setiap query kepada AI memiliki harga—bukan hanya dalam dolar, tapi dalam ton CO₂ dan liter air."*
