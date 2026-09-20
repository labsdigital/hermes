---
name: exam-preparation
description: Generate HOTS exam questions for Indonesian students SD-SMA.
---

# Exam Preparation Skill — Multi-Level Question Generation

## Philosophy

**Progression, bukan lompatan** — Each student needs strong foundation before HOTS.

### Bloom's Taxonomy Modified

```
Level 1: REMEMBER    (Mudah)     → Recall facts, definitions
Level 2: UNDERSTAND  (Mudah-Sd)  → Explain in own words
Level 3: APPLY       (Sedang)    → Apply concepts to new situations
Level 4: ANALYZE     (Sedang-St) → Compare, analyze relationships
Level 5: EVALUATE & CREATE (HOTS) → Judge, justify, create solutions
```

## Question Distribution

| Level | % of Total | Count (12 soal) |
|-------|------------|-----------------|
| 1 - Remember | 15-20% | 2 soal |
| 2 - Understand | 15-20% | 2 soal |
| 3 - Apply | 25-30% | 3 soal |
| 4 - Analyze | 20-25% | 3 soal |
| 5 - HOTS | 15-20% | 2 soal |

## Topics by Level

### Matematika
- **SD 1-3**: Bilangan, penjumlahan-pengurangan, perkalian dasar
- **SD 4-6**: Pecahan, desimal, luas-keliling, volume
- **SMP 7-9**: Aljabar, persamaan linear, geometri, statistik
- **SMA 10-12**: Fungsi, trigonometri, kalkulus, logaritma

### IPA
- **SD**: Makhluk hidup, gaya, energi, ekosistem
- **SMP**: Gerak & gaya, gelombang, atom, bioteknologi
- **SMA**: Fisika lanjut, kimia, biologi, ekosistem kompleks

### Literasi/Bahasa
- **SD**: Pemahaman teks, kosakata, tata bahasa
- **SMP**: Analisis teks argumentatif, puisi, drama
- **SMA**: Esai kompleks, kritik teks, sastra, retorika

## Question Types

### MC (Pilihan Ganda)
- 4 opsi (A-D) untuk SD; 4-5 untuk SMP/SMA
- 1 jawaban benar, 3 distraktor plausibel
- Hindari: "semua benar/salah"

### MCMA (Pilihan Ganda Kompleks)
- "Pernyataan mana yang BENAR?" (checkbox)
- Cocok untuk Level 4-5

### Isian Singkat
- Jawaban 1-3 kata atau 1 kalimat
- Cocok untuk Level 1-2

### Essay/Uraian
- Jawaban 3-10 kalimat
- Sertakan rubrik penilaian
- Cocok untuk Level 4-5

## Output Format

```markdown
# Paket Latihan Ujian Akhir [SUBJEK] [JENJANG]

## 📚 Profil Paket
| Parameter | Value |
|-----------|-------|
| Jenjang | SD/SMP/SMA Kelas X |
| Subjek | [Subject] |
| Topik | [Topic] |
| Total Soal | [N] soal |
| Jenis Soal | [Type] |
| Waktu Ideal | [X] menit |

## SOAL LEVEL 1 - REMEMBER
### Soal 1
[Soal + Opsi]

**Kunci Jawaban:** [Letter]

**Pembahasan:**
1. Langkah 1
2. Langkah 2
3. Hasil

**Kesalahan umum siswa:**
- Error 1
- Error 2

... (lanjutkan Level 2-5) ...

## 📊 Strategi Pembelajaran
[Berikut strategi untuk setiap level]

## 📌 Catatan untuk Guru/Orang Tua
[Common errors, tips, pengayaan]
```

## HOTS Question Framework

### Framework A: Real-World Problem Modeling
1. Start from authentic scenario
2. Add math/science angle
3. Create multi-concept integration
4. Require justification

### Framework B: Cognitive Demand Progression
```
Level 1: Recall formula
    ↓ Add context
Level 2: Explain concept
    ↓ Add application  
Level 3: Solve standard problem
    ↓ Add analysis
Level 4: Compare/analyze scenarios
    ↓ Add judgment
Level 5: Optimize/evaluate with constraints
```

### HOTS Checklist
- [ ] Open-ended (multiple valid answers possible)
- [ ] Requires justification & reasoning
- [ ] Complex or ambiguous context
- [ ] Needs judgment or creativity
- [ ] Transferable to other contexts
- [ ] Authentic real-world relevance

## File Output

Save to: `/opt/data/hermes/<agent>/reports/`

Formats:
- `.md` — Full markdown with detailed pembahasan
- `.html` — Styled exam format with print support

### ⚠️ Git Workspace & Submodule Workflow (CRITICAL)

The `/opt/data` directory is the **parent repo**, and `hermes/` is a **git submodule** (mode `160000` in `git ls-files`). This means:

1. **Git operations must run inside the submodule:**
   ```bash
   cd /opt/data/hermes
   git add <path>           # stage from within submodule
   git commit -m "..."     # commit to submodule
   git push origin main     # push from within submodule
   ```

2. **Files are at `/opt/data/hermes/<agent>/reports/` but git commands run from `/opt/data/hermes/`**
   Always `cd /opt/data/hermes` before staging, committing, or pushing exam files.

3. **`git add` on already-staged files is a no-op for staging status:**
   If a file is already in the index, `git add <path>` updates its content but does NOT change the "Changes to be committed" status. To verify what's actually staged:
   ```bash
   git ls-files --stage <path>     # check index state
   git diff --cached               # see what's staged
   git diff                        # see unstaged changes
   ```

4. **Before generating new files, check for existing work:**
   ```bash
   ls /opt/data/hermes/<agent>/reports/    # existing files
   git log --oneline -5                    # recent commits
   ```
   Previous sessions may have already created similar files (e.g. `soal-ujian-matematika-sd-kelas-5-2026-08-28.md`). Always check before creating to avoid duplication.

### HTML Exam Styling (Recommended)

For the HTML version, use this interactive toggle pattern:

```html
<style>
.answer-content { display: none; }
.answer-content.show { display: block; }
</style>

<button class="answer-toggle" onclick="toggleAnswer(this)">
  🔍 Lihat Kunci Jawaban & Pembahasan
</button>
<div class="answer-content">
  <!-- kunci + pembahasan here -->
</div>

<script>
function toggleAnswer(btn) {
  const c = btn.nextElementSibling;
  if (c.classList.contains('show')) {
    c.classList.remove('show');
    btn.textContent = '🔍 Lihat Kunci Jawaban & Pembahasan';
  } else {
    c.classList.add('show');
    btn.textContent = '🙈 Sembunyikan Pembahasan';
  }
}
</script>
```

Include: level-colored badges (L1=blue, L2=green, L3=amber, L4=red, L5=purple), distribution bar chart, answer key summary table, and strategy section per level. Print styles should hide all `.answer-content` by default.

## Example Prompt

```
@minerva latihan ujian akhir Matematika SD kelas 5
@minerva buat soal HOTS IPA tentang ekosistem
@minerva soal progression Persamaan Linear SMP kelas 8
```
