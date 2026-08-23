# PRD: Rasio & Perbandingan — Presentasi Interaktif

**Document Version:** 1.0.0  
**Status:** ✅ Approved  
**Last Updated:** 2026-08-23  
**Author:** @elon (Web Development Specialist)  
**Project:** Hermes Multi-Agent System — Educational Content

---

## 1. Executive Summary

### 1.1 Product Overview
Rasio & Perbandingan adalah presentasi interaktif berbasis web (single HTML file) yang dirancang untuk mengajarkan konsep rasio dan perbandingan kepada siswa Sekolah Dasar (SD). Presentasi ini menggabungkan konten edukatif dengan elemen interaktif untuk meningkatkan pemahaman dan engagement pembelajaran.

### 1.2 Objectives
- ✅ Menyederhanakan konsep matematika rasio untuk anak SD
- ✅ Memberikan pengalaman belajar interaktif melalui lab dan simulasi
- ✅ Memudahkan guru dalam presentasi materi di kelas
- ✅ Meningkatkan pemahaman visual melalui animasi dan visualisasi
- ✅ Mendukung pembelajaran mandiri dengan quiz dan refleksi

### 1.3 Target Users
| User Type | Description | Use Case |
|-----------|-------------|----------|
| **Siswa SD** | Anak kelas 4-6 SD (umur 9-12 tahun) | Belajar rasio dengan cara yang menyenangkan |
| **Guru** | Guru matematika SD | Media presentasi di kelas |
| **Orang Tua** | Orang tua yang mendampingi belajar | Bantuan belajar di rumah |

---

## 2. Design System — MyStyle1

### 2.1 Color Palette
```css
/* Primary Colors */
--color-primary-dark: #0f172a;  /* Slate 900 — Text utama, judul */
--color-primary-white: #ffffff;  /* White — Background cards, clean areas */
--color-accent-orange: #f97316;  /* Orange 500 — Highlights, buttons, accents */
--color-background-light: #f8fafc;  /* Slate 50 — Slide background */

/* Secondary Colors */
--color-text-muted: #64748b;  /* Slate 500 — Subtitle, caption */
--color-border-soft: #e2e8f0;  /* Slate 200 — Borders, dividers */
```

### 2.2 Typography Scale (Inter Font)
| Element | Size Range | Weight | Usage |
|---------|------------|--------|-------|
| **App Title** | 56-72px | 800 (ExtraBold) | UPPERCASE, judul aplikasi |
| **Chapter Divider** | 96-120px | 900 (Black) | Judul bab besar, full-bleed |
| **Section Heading** | 48-64px | 700 (Bold) | Judul section/subsection |
| **Subheading** | 32-40px | 600 (SemiBold) | Sub-judul, label |
| **Body Text** | 24-28px | 400 (Regular) | Konten utama, paragraf |
| **Caption** | 18-20px | 500 (Medium) | Keterangan, footnote |

### 2.3 Design Principles
- **Clean & Professional:** Apple/Google design language
- **Visual Hierarchy:** Size contrast jelas antara judul, subjudul, body
- **Minimalist:** Kurangi elemen dekoratif yang tidak perlu
- **Accessible:** Kontras tinggi, font mudah dibaca
- **Interactive:** Animasi smooth, feedback visual jelas

---

## 3. Content Structure

### 3.1 Slide Overview (41 Slides Total)

```
═══════════════════════════════════════════════════════════
                    PEMBUKA (2 slides)
═══════════════════════════════════════════════════════════
Slide 1:  Title — "RASIO & PERBANDINGAN" (UPPERCASE)
Slide 2:  Agenda — Tujuan pembelajaran

═══════════════════════════════════════════════════════════
                   BAB 1: KONSEP DASAR (5 slides)
═══════════════════════════════════════════════════════════
Slide 3:  🟠 DIVIDER — "BAB 1" (96-120px, full-bleed orange)
Slide 4:  Apa itu Rasio? — Definisi visual
Slide 5:  Contoh: Buah-buahan — Apel vs Jeruk
Slide 6:  Cara Menulis Rasio — Notasi a:b, a/b
Slide 7:  Menyederhanakan Rasio — Konsep FPB

═══════════════════════════════════════════════════════════
               LAB PENYEDERHANAAN (4 slides)
═══════════════════════════════════════════════════════════
Slide 8:   Lab 1: Penyederhanaan - Buah (interaktif)
Slide 9:   Lab 2: Penyederhanaan - Hewan (interaktif)
Slide 10:  Lab 3: Penyederhanaan - Kendaraan (interaktif)
Slide 11:  Lab 4: Quiz Penyederhanaan (skor tracking)

═══════════════════════════════════════════════════════════
              BAB 2: PERBANDINGAN SENILAI (7 slides)
═══════════════════════════════════════════════════════════
Slide 12:  🟠 DIVIDER — "BAB 2"
Slide 13:  Pengantar Perbandingan Senilai
Slide 14:  Rumus dan Konsep — y = k × x
Slide 15:  Contoh: Harga Barang
Slide 16:  Contoh: Jumlah Makanan
Slide 17:  Lab 5: Slider Senilai - Harga (interaktif)
Slide 18:  Lab 6: Slider Senilai - Makanan (interaktif)
Slide 19:  Latihan Senilai

═══════════════════════════════════════════════════════════
           BAB 3: PERBANDINGAN BERBALIK NILAI (7 slides)
═══════════════════════════════════════════════════════════
Slide 20:  🟠 DIVIDER — "BAB 3"
Slide 21:  Pengantar Perbandingan Berbalik Nilai
Slide 22:  Rumus dan Konsep — x × y = k
Slide 23:  Contoh: Tukang dan Hari
Slide 24:  Contoh: Kambing dan Rumput
Slide 25:  Lab 7: Slider Berbalik - Tukang (interaktif)
Slide 26:  Lab 8: Slider Berbalik - Kambing (interaktif)
Slide 27:  Latihan Berbalik

═══════════════════════════════════════════════════════════
               BAB 4: SIMULASI VISUAL (4 slides)
═══════════════════════════════════════════════════════════
Slide 28:  🟠 DIVIDER — "BAB 4"
Slide 29:  Simulasi Perbandingan Hewan
Slide 30:  Simulasi Perbandingan Kendaraan
Slide 31:  Quiz Campuran

═══════════════════════════════════════════════════════════
               BAB 5: MISI DUNIA NYATA (4 slides)
═══════════════════════════════════════════════════════════
Slide 32:  🟠 DIVIDER — "BAB 5"
Slide 33:  Misi 1: Belanja
Slide 34:  Misi 2: Resep Masakan
Slide 35:  Misi 3: Peta dan Skala

═══════════════════════════════════════════════════════════
                    PENUTUP (5 slides)
═══════════════════════════════════════════════════════════
Slide 36:  Refleksi — 3 pertanyaan renungan
Slide 37:  Ringkasan — Poin-poin penting
Slide 38:  Tips Mengingat
Slide 39:  🟠 DIVIDER — "QUESTIONS?"
Slide 40:  Thank You
Slide 41:  Penutup

═══════════════════════════════════════════════════════════
```

### 3.2 Chapter Dividers
Setiap bab dimulai dengan slide divider yang membedakan secara visual:
- **Background:** Full-bleed orange (#f97316)
- **Typography:** "BAB X" ukuran 96-120px, white, font-weight 900
- **Position:** Centered, vertikal dan horizontal
- **Effect:** Ghost number background (opacity rendah)

---

## 4. Interactive Features — 10 Labs

### 4.1 Lab Penyederhanaan (4 Labs)

#### Lab 1: Penyederhanaan - Buah
```
Input:  Jumlah Apel : Jumlah Jeruk
Output: Rasio sederhana + FPB
Visual: Ikon buah yang berubah sesuai input
Interaksi: Input angka → Auto-simplify dengan GCD
```

#### Lab 2: Penyederhanaan - Hewan
```
Input:  Jumlah Kucing : Jumlah Burung
Output: Rasio sederhana + penjelasan
Visual: Ikon kucing 🐱 dan burung 🐦
Contoh: 8:4 → 2:1
```

#### Lab 3: Penyederhanaan - Kendaraan
```
Input:  Jumlah Motor : Jumlah Mobil
Output: Rasio + Total Roda + Rasio Roda
Visual: Ikon motor 🏍️ dan mobil 🚗
Kalkulasi: Roda motor (2) × jumlah + Roda mobil (4) × jumlah
```

#### Lab 4: Quiz Penyederhanaan
```
Format: 3 soal pilihan ganda
Feedback: Benar/Salah + penjelasan
Scoring: Track skor, lock jawaban setelah dijawab
```

### 4.2 Lab Perbandingan Senilai (2 Labs)

#### Lab 5: Slider Senilai - Harga
```
Input:  Slider jumlah barang (1-12)
Output: Tabel harga + Grafik garis lurus
Rumus: Harga_total = Harga_satuan × Jumlah
Visual: SVG chart garis teal melewati origin
```

#### Lab 6: Slider Senilai - Makanan
```
Input:  Slider jumlah anak
Output: Jumlah donat/makanan yang dibutuhkan
Rumus: Donat = Anak × 2
Visual: Ikon donat 🍩 yang bertambah sesuai slider
```

### 4.3 Lab Perbandingan Berbalik Nilai (2 Labs)

#### Lab 7: Slider Berbalik - Tukang
```
Input:  Slider jumlah pekerja
Output: Waktu selesai (hari)
Rumus: Pekerja × Hari = Konstanta (contoh: 12工人×6 hari = 72)
Visual: Bar chart yang berkurang saat pekerja bertambah
```

#### Lab 8: Slider Berbalik - Kambing
```
Input:  Slider jumlah kambing
Output: Hari rumput bertahan
Rumus: Kambing × Hari = Konstanta
Visual: Ikon kambing + rumput 🌿
```

### 4.4 Lab Visual & Quiz (2 Labs)

#### Lab 9: Mixing Visual
```
Input:  Ratio Warna A : Warna B
Output: Warna campuran + persentase
Visual: Gradient warna yang berubah real-time
Interaksi: Dual slider untuk masing-masing warna
```

#### Lab 10: Tebak Rasio
```
Format: Soal acak tentang perbandingan
Feedback: Benar/Salah + penjelasan
Level: Mudah → Sulit
```

---

## 5. Navigation System

### 5.1 Navigation Elements
```
┌─────────────────────────────────────────────────────────┐
│  [Progress Bar]                                    [01/41]│
│                                                         │
│                     SLIDE CONTENT                       │
│                                                         │
│                                                         │
│                              [🏠] [◀]     [▶]          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Navigation Buttons
| Button | Icon | Function | Position |
|--------|------|----------|----------|
| **Home** | SVG 🏠 | Jump to slide 1 | Bottom-right |
| **Prev** | SVG ◀ | Previous slide | Bottom-right |
| **Next** | SVG ▶ | Next slide | Bottom-right |

### 5.3 Interactive Features
- **Keyboard Navigation:** Arrow keys (← →)
- **Touch/Swipe:** Mobile support
- **Deep Linking:** URL hash (#slide-number)
- **Progress Bar:** Visual indicator di atas
- **Slide Counter:** Current / Total

### 5.4 Button Design
- **Style:** Pill shape dengan SVG icon
- **Shadow:** Layered soft shadow
- **Hover:** Lift effect + orange fill
- **Active:** Scale animation
- **Disabled:** Grayed out at boundaries

---

## 6. Technical Specifications

### 6.1 File Structure
```
/opt/data/hermes/elon/
├── rasio-perbandingan-v4.html    # Main file (85 KB)
├── rasio-perbandingan-v3.html    # Previous version (SD Level)
├── rasio-perbandingan-v2.html    # Previous version (Professional)
├── rasio-perbandingan-lengkap.html  # Previous version (29 slides)
└── AGENTS.md                     # Subagent documentation
```

### 6.2 Technology Stack
```
Frontend:
├── HTML5 (Semantic)
├── CSS3 (Modern Features)
│   ├── CSS Variables (Design Tokens)
│   ├── Flexbox & Grid Layout
│   ├── Animations & Transitions
│   └── Responsive Design
└── JavaScript (ES6+)
    ├── Vanilla JS (No Framework)
    ├── DOM Manipulation
    ├── Event Handling
    └── Local State Management
```

### 6.3 External Dependencies
```
Fonts:
└── Inter (Google Fonts)
    - Weights: 400, 500, 600, 700, 800, 900

Icons:
└── Inline SVG (No external library)
```

### 6.4 Browser Compatibility
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ Mobile Safari/Chrome

---

## 7. Content Guidelines

### 7.1 Language & Tone
- **Bahasa:** Indonesia
- **Level:** SD (Kelas 4-6)
- **Tone:** Sopan, edukatif, menyenangkan
- **Vocabulary:** Sederhana, tidak teknis

### 7.2 Content Rules
1. **Minimum Text:** Kurangi teks panjang, gunakan poin-poin
2. **Visual First:** Prioritaskan gambar/ikon dibanding teks
3. **Examples:** Gunakan contoh sehari-hari (buah, hewan, makanan)
4. **Interactive:** Setiap konsep memiliki contoh interaktif
5. **Emoji:** Maksimal 1 emoji per slide untuk dekorasi

### 7.3 Learning Objectives
Setelah menyelesaikan presentasi, siswa mampu:
1. ✅ Menjelaskan pengertian rasio
2. ✅ Menulis rasio dalam berbagai notasi
3. ✅ Menyederhanakan rasio dengan FPB
4. ✅ Mengidentifikasi perbandingan senilai
5. ✅ Mengidentifikasi perbandingan berbalik nilai
6. ✅ Menerapkan konsep dalam kehidupan sehari-hari

---

## 8. Quality Assurance

### 8.1 Validation Checklist
- [x] Slide count: 41 slides
- [x] Chapter dividers: 6 (Bab 1-5 + Questions)
- [x] Interactive labs: 10 labs
- [x] JavaScript syntax: Valid
- [x] HTML tag balance: Correct
- [x] ID references: All present
- [x] Keyboard navigation: Working
- [x] Touch/swipe: Working
- [x] Deep linking: Working
- [x] Responsive design: Tested
- [x] Cross-browser: Compatible

### 8.2 Testing Scenarios
1. **Navigation Test:** All slides accessible via keyboard and buttons
2. **Lab Interaction Test:** All 10 labs function correctly
3. **Quiz Test:** Scoring and feedback working
4. **Slider Test:** Real-time updates on all sliders
5. **Responsive Test:** Works on desktop, tablet, mobile
6. **Performance Test:** Load time < 2 seconds

---

## 9. Version History

| Version | Date | Slides | Changes |
|---------|------|--------|---------|
| v1 | 2026-08-23 | 15 | Initial version with labs |
| Lengkap | 2026-08-23 | 29 | Added senilai & berbalik nilai |
| v2 | 2026-08-23 | 29 | MyStyle1 professional design |
| v3 | 2026-08-23 | 30 | SD level, home button, minimal emoji |
| **v4** | **2026-08-23** | **41** | **Chapter dividers, 10 labs, UPPERCASE title** |

---

## 10. File Locations

### 10.1 Primary File
```
Path: /opt/data/hermes/elon/rasio-perbandingan-v4.html
Size: 85 KB (1,555 lines)
Commit: 5de88ce
Branch: main
Repository: https://github.com/labsdigital/hermes
```

### 10.2 GitHub URL
```
https://github.com/labsdigital/hermes/tree/main/elon
https://labsdigital.github.io/hermes/elon/rasio-perbandingan-v4.html
```

---

## 11. Future Enhancements

### 11.1 Potential Features
- [ ] Audio narration for each slide
- [ ] Print-friendly version
- [ ] Offline mode (PWA)
- [ ] Multiple language support
- [ ] Progress saving (localStorage)
- [ ] Teacher dashboard
- [ ] Export to PDF
- [ ] Embeddable widget

### 11.2 Content Expansion
- [ ] Advanced rasio problems
- [ ] Geometry applications
- [ ] Statistics introduction
- [ ] Real-world case studies

---

## 12. Approval & Sign-off

| Role | Name | Date | Status |
|------|------|------|--------|
| **Product Owner** | Master Tamim | 2026-08-23 | ✅ Approved |
| **Content Lead** | @max | 2026-08-23 | ✅ Reviewed |
| **Design Lead** | @elon | 2026-08-23 | ✅ Approved |
| **Tech Lead** | @zetta | 2026-08-23 | ✅ Approved |

---

**Document End**
