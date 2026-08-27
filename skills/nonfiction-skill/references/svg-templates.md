# SVG Templates for Atlas Essays

Koleksi template SVG yang siap pakai untuk ilustrasi esai non-fiksi Atlas.

## Template 1: Perbandingan Dua Konsep (Default)

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" role="img" aria-labelledby="svg-title svg-desc">
  <title id="svg-title">Judul Ilustrasi</title>
  <desc id="svg-desc">Deskripsi singkat ilustrasi.</desc>
  
  <rect width="800" height="400" fill="#f8fafc"/>
  
  <!-- LEFT: Positive/Concept A -->
  <g transform="translate(0, 0)">
    <rect x="20" y="20" width="370" height="360" rx="20" fill="#f0fdf4" stroke="#86efac" stroke-width="2"/>
    <!-- Add your visual elements here -->
    <text x="205" y="370" text-anchor="middle" font-family="Georgia, serif" font-size="20" fill="#166534" font-weight="bold">Konsep A</text>
  </g>
  
  <!-- RIGHT: Negative/Concept B -->
  <g transform="translate(410, 0)">
    <rect x="20" y="20" width="370" height="360" rx="20" fill="#eff6ff" stroke="#bfdbfe" stroke-width="2"/>
    <!-- Add your visual elements here -->
    <text x="205" y="370" text-anchor="middle" font-family="Georgia, serif" font-size="20" fill="#1e3a8a" font-weight="bold">Konsep B</text>
  </g>
  
  <line x1="395" y1="20" x2="395" y2="380" stroke="#e2e8f0" stroke-width="2" stroke-dasharray="8,4"/>
  
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#94a3b8"/>
    </marker>
  </defs>
</svg>
```

## Template 2: Flowchart Proses

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 300" role="img" aria-labelledby="flow-title">
  <title id="flow-title">Alur Proses</title>
  
  <rect width="800" height="300" fill="#f8fafc"/>
  
  <!-- Step 1 -->
  <rect x="50" y="100" width="160" height="100" rx="10" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
  <text x="130" y="145" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#1e40af">Input</text>
  <text x="130" y="170" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Langkah 1</text>
  
  <!-- Arrow 1 -->
  <line x1="210" y1="150" x2="250" y2="150" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>
  
  <!-- Step 2 -->
  <rect x="260" y="100" width="160" height="100" rx="10" fill="#fef3c7" stroke="#f59e0b" stroke-width="2"/>
  <text x="340" y="145" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#78350f">Proses</text>
  <text x="340" y="170" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Langkah 2</text>
  
  <!-- Arrow 2 -->
  <line x1="420" y1="150" x2="460" y2="150" stroke="#94a3b8" stroke-width="2" marker-end="url(#arrow)"/>
  
  <!-- Step 3 -->
  <rect x="470" y="100" width="160" height="100" rx="10" fill="#dcfce7" stroke="#22c55e" stroke-width="2"/>
  <text x="550" y="145" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#14532d">Output</text>
  <text x="550" y="170" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Langkah 3</text>
  
  <defs>
    <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0,0 L8,4 L0,8 Z" fill="#94a3b8"/>
    </marker>
  </defs>
</svg>
```

## Template 3: Timeline Horizontal

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 200" role="img" aria-labelledby="timeline-title">
  <title id="timeline-title">Timeline Evolusi</title>
  
  <rect width="800" height="200" fill="#f8fafc"/>
  
  <!-- Timeline line -->
  <line x1="50" y1="100" x2="750" y2="100" stroke="#94a3b8" stroke-width="3"/>
  
  <!-- Point 1 -->
  <circle cx="100" cy="100" r="12" fill="#3b82f6"/>
  <text x="100" y="80" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#1e40af">1950</text>
  <text x="100" y="130" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Awal</text>
  
  <!-- Point 2 -->
  <circle cx="300" cy="100" r="12" fill="#f59e0b"/>
  <text x="300" y="80" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#78350f">1990</text>
  <text x="300" y="130" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Perkembangan</text>
  
  <!-- Point 3 -->
  <circle cx="500" cy="100" r="12" fill="#22c55e"/>
  <text x="500" y="80" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#14532d">2020</text>
  <text x="500" y="130" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Revolusi</text>
  
  <!-- Point 4 -->
  <circle cx="700" cy="100" r="12" fill="#ef4444"/>
  <text x="700" y="80" text-anchor="middle" font-family="Georgia, serif" font-size="14" fill="#991b1b">2026</text>
  <text x="700" y="130" text-anchor="middle" font-family="Georgia, serif" font-size="12" fill="#64748b">Sekarang</text>
</svg>
```

## Template 4: Icon Set (Human vs Machine)

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 200" role="img" aria-labelledby="icon-title">
  <title id="icon-title">Perbandingan Manusia dan Mesin</title>
  
  <rect width="400" height="200" fill="#f8fafc"/>
  
  <!-- Human icon (left) -->
  <g transform="translate(100, 60)">
    <circle cx="40" cy="40" r="35" fill="#fed7aa" opacity="0.8"/>
    <path d="M20 80 Q40 100 60 80" fill="none" stroke="#fdba74" stroke-width="4" stroke-linecap="round"/>
    <!-- Brain waves -->
    <path d="M15 30 Q40 10 65 30" fill="none" stroke="#fb923c" stroke-width="2"/>
    <path d="M15 20 Q40 0 65 20" fill="none" stroke="#f97316" stroke-width="2"/>
    <text x="40" y="120" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#7c2d12" font-weight="bold">Manusia</text>
  </g>
  
  <!-- Machine icon (right) -->
  <g transform="translate(240, 60)">
    <rect x="10" y="10" width="60" height="60" rx="8" fill="#dbeafe" stroke="#3b82f6" stroke-width="2"/>
    <rect x="25" y="25" width="30" height="30" rx="4" fill="#bfdbfe"/>
    <!-- Circuit lines -->
    <line x1="40" y1="10" x2="40" y2="0" stroke="#3b82f6" stroke-width="2"/>
    <line x1="40" y1="70" x2="40" y2="80" stroke="#3b82f6" stroke-width="2"/>
    <line x1="10" y1="40" x2="0" y2="40" stroke="#3b82f6" stroke-width="2"/>
    <line x1="70" y1="40" x2="80" y2="40" stroke="#3b82f6" stroke-width="2"/>
    <text x="40" y="120" text-anchor="middle" font-family="Georgia, serif" font-size="16" fill="#1e3a8a" font-weight="bold">Mesin</text>
  </g>
</svg>
```

## Palette Warna Atlas

| Warna | Hex | Usage |
|-------|-----|-------|
| Emerald (positif) | `#22c55e` | Healthy, growth, nature |
| Green dark | `#166534` | Text labels (positive) |
| Red (negatif) | `#ef4444` | Warning, decay, danger |
| Red dark | `#991b1b` | Text labels (negative) |
| Blue (netral) | `#3b82f6` | Tech, data, process |
| Blue dark | `#1e3a8a` | Text labels (neutral) |
| Orange (hangat) | `#f97316` | Human, warmth, emotion |
| Orange dark | `#7c2d12` | Text labels (warm) |
| Amber (cahaya) | `#fbbf24` | Light, ideas, inspiration |
| Slate bg | `#f8fafc` | Background |
| Green bg | `#f0fdf4` | Positive card bg |
| Blue bg | `#eff6ff` | Neutral card bg |
| Orange bg | `#fff7ed` | Warm card bg |
| Red bg | `#fef2f2` | Negative card bg |

## Tips SVG untuk Email

1. **Inline attributes** — jangan gunakan `<style>` blocks
2. **UTF-8 declaration** — wajib untuk text non-ASCII
3. **Simple shapes** — hindari gradient kompleks
4. **Test dulu** — `xmllint --noout file.svg` sebelum embed
5. **Size < 10KB** — untuk loading cepat di email client
