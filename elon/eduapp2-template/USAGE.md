# Usage Guide — EduApp2 Template

## Quick Start

### 1. Clone Template
```bash
# Dari repo hermes
cp elon/eduapp2-template/index.html elon/[your-project]/index.html
mkdir -p elon/[your-project]
cp elon/eduapp2-template/index.html elon/[your-project]/
```

### 2. Edit Template

#### A. Header (Lines 1-10)
```html
<title>[JUDUL APLIKASI] — [SUBJEC]</title>
```

#### B. Topbar Title (Line 161)
```html
<span class="tb-title">[JUDUL APLIKASI]<span class="tb-badge">LAB</span></span>
```

#### C. Sidebar Logo (Lines 169-171)
```html
<div class="sb-title">[JUDUL APLIKASI]</div>
<div class="sb-sub">[SUBJEC]</div>
```

#### D. Navigation (Lines 180-280)
Edit setiap `<button class="sb-item">` sesuai jumlah slide:
```html
<button class="sb-item" onclick="go(N)" data-slide="N">
  <span class="sb-num">XX</span>
  <span class="sb-txt">
    <span class="sb-t">[Judul Slide]</span>
    <span class="sb-s">[Deskripsi singkat]</span>
  </span>
</button>
```

#### E. Slide Content (Lines 300+)
Setiap slide memiliki struktur:
```html
<div class="slide" id="slide-N">
  <div class="inner">
    <div class="frame">
      <div class="frame-top">
        <span class="kicker">[Bab Label]</span>
        <span class="fcount">N / 30</span>
      </div>
      <div class="frame-body">
        <h2 class="st reveal">[Judul Slide]</h2>
        <!-- Konten di sini -->
      </div>
    </div>
  </div>
</div>
```

### 3. Tambah Quiz Data

Di bagian JavaScript (bawah file), edit `QUIZ_DATA`:
```javascript
const QUIZ_DATA = {
  1: [
    {
      q: "Pertanyaan 1?",
      opts: ["Opsi A", "Opsi B", "Opsi C", "Opsi D"],
      correct: 0,
      exp: "Penjelasan jawaban benar"
    },
    // ... tambah 4 soal lagi
  ],
  2: [...],
  final: [...]
};
```

### 4. Implementasi Simulasi

Untuk canvas simulation, tambahkan di function `initSim()`:
```javascript
function initSim() {
  const canvas = document.getElementById('simCanvas');
  const ctx = canvas.getContext('2d');
  
  // Setup canvas size
  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = 420;
  
  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Draw your simulation here
    requestAnimationFrame(animate);
  }
  animate();
}
```

## Komponen UI yang Tersedia

### Card
```html
<div class="card">
  <div class="kicker mb1">Label</div>
  <p class="caption">Konten</p>
</div>
```

### Formula Box
```html
<div class="formula">
  <div class="fx">x = v₀ · cos(θ) · t</div>
  <div class="ex">keterangan</div>
</div>
```

### Analogy Box
```html
<div class="analogy">
  <div class="atitle">💡 Analogi</div>
  <p class="caption">Penjelasan</p>
</div>
```

### Stats Grid
```html
<div class="grid4">
  <div class="stat-chip"><b>10</b><span>Slide</span></div>
  <!-- ... -->
</div>
```

### List Sifat
```html
<ul class="sifat">
  <li>Poin pertama</li>
  <li>Poin kedua</li>
</ul>
```

## Keyboard Shortcuts
- `→` / `↓` : Slide selanjutnya
- `←` / `↑` : Slide sebelumnya
- `Home` : Kembali ke slide pertama
- `End` : Langsung ke slide terakhir

## Mobile
- Swipe kiri/kanan untuk navigasi
- Hamburger menu untuk sidebar
- FAB buttons tetap muncul

## Print
- Sidebar & topbar tersembunyi
- Semua slide tampil (page break after each)
- Cocok untuk PDF export

## Troubleshooting

### Animasi tidak jalan
Pastikan `requestAnimationFrame` dipanggil dan ada update state di loop.

### Quiz tidak muncul
Cek apakah `initQuiz()` dipanggil saat slide aktif.

### Canvas tidak resize
Tambahkan event listener `window.addEventListener('resize', resizeCanvas)`.

## Contoh Implementasi
- `elon/gerak-parabola/` — Fisika simulasi
- `elon/computational-thinking-v3/` — CT learning app
- `elon/rangkaian-listrik-v2/` — Electric circuits
