# Skill: Masnavi Rumi Research

## Description
Mencari, menganalisis, dan menyajikan karya-karya Jalaludin Rumi (Mawlana) dari Masnavi-ye Ma'navi dan Divan-e Shams. Menggunakan API publik masnavi.ai untuk akurasi dan verifikasi.

## Trigger
Gunakan skill ini ketika user meminta:
- Kutipan dari Rumi/Masnavi
- Penjelasan tentang tema tertentu dalam puisi Rumi
- Verifikasi kutipan
- Analisis filosofis dari beyt tertentu
- Pencarian berdasarkan makna (bukan hanya teks)

## Steps

### 1. Understand Request
Tentukan jenis query:
- **Semantic search**: User memberikan konsep/tema → gunakan `search_meaning`
- **Text search**: User memberikan teks Persia → gunakan `search`
- **Lookup**: User memberikan referensi spesifik → gunakan `lookup`
- **Verify**: User ingin mengecek keaslian kutipan → gunakan `verify`

### 2. API Query
Gunakan format curl:

```bash
# Semantic search (most common)
curl -s "https://masnavi.ai/api/search_meaning?q={query}&limit=10"

# Text search (Persian)
curl -s "https://masnavi.ai/api/search?q={persian_text}&limit=10"

# Lookup specific beyt
curl -s "https://masnavi.ai/api/lookup?citation=M1:1"

# Verify quote authenticity
curl -s "https://masnavi.ai/api/verify?text={text}"

# Get section
curl -s "https://masnavi.ai/api/get_section?section_id=M1:1-10"

# Random beyt
curl -s "https://masnavi.ai/api/random_beyt?daftar=1"
```

### 3. Parse Response
Response JSON memiliki struktur:
```json
{
  "results": [
    {
      "citation": "M1:1",
      "daftar": 1,
      "beyt_number": 1,
      "hemistich_1": "بشنو این نی چون شکایت می‌کند",
      "hemistich_2": "از جدایی‌ها حکایت می‌کند",
      "section": "The Reed Flute",
      "score": 0.95
    }
  ]
}
```

### 4. Format Output
Buat artikel dengan struktur:

```markdown
# [Judul Tema]

## Kutipan Rumi

> [Hemistich 1] [Hemistich 2]
> — M{daftar}:{beyt}

### Terjemahan
[Indonesian translation]

### Makna & Konteks
[Philosophical explanation]

## Kutipan Terkait

[Beyts lain yang relevan]

---
Sumber: masnavi.ai
```

### 5. Save & Report
- Simpan ke `chalbi/reports/<tema>-YYYY-MM-DD.md`
- Commit ke GitHub
- Laporkan ke user

## Key Concepts

### Citation Format
- **M{daftar}:{beyt}** - Masnavi citation
- **G{ghazal}:{beyt}** - Divan citation
- **g:{n}** - Global index (1-25635)

### Structure of Masnavi
- **6 Daftars** (Books):
  1. Daftar 1: Spiritual awakening
  2. Daftar 2: Love and longing
  3. Daftar 3: Mystical themes
  4. Daftar 4: Ethical teachings
  5. Daftar 5: Stories and parables
  6. Daftar 6: Ultimate truths

### Common Themes
- **Eshq** (عشق) - Divine love
- **Jamal** (جمال) - Beauty
- **Fana** (فنا) - Annihilation in God
- **Wahdat al-Wujud** (وحدت الوجود) - Unity of Being
- **Ney** (نی) - Reed flute metaphor
- **Mey** (می) - Wine of spiritual intoxication

## Best Practices

1. **Always verify** before publishing quotes
2. **Include original Persian text** with every translation
3. **Provide citation** in M{daftar}:{beyt} format
4. **Explain context** - Rumi's poetry is deeply philosophical
5. **Use semantic search** for conceptual queries
6. **Cross-reference** with Divan when relevant
7. **Respect the tradition** - Rumi is sacred to many

## Error Handling

If API returns error:
```bash
# Check API status
curl -s "https://masnavi.ai/api/search_meaning?q=test&limit=1"

# Try alternative endpoint
curl -s "https://masnavi.ai/api/search?q=test&limit=1"

# Fall back to static corpus
curl -s "https://masnavi.ai/corpus.jsonl" | head -20
```

## Output Examples

### Example 1: Semantic Search
User: "Apa kata Rumi tentang cinta?"

```bash
curl -s "https://masnavi.ai/api/search_meaning?q=love&limit=5"
```

Output: List of 5 most relevant beyts with citations.

### Example 2: Lookup Specific Beyt
User: "Jelaskan M1:1"

```bash
curl -s "https://masnavi.ai/api/lookup?citation=M1:1"
```

Output: Full beyt with both hemistichs and explanation.

### Example 3: Verify Quote
User: "Apakah ini kutipan Rumi: 'bast thou heard the reed...'"

```bash
curl -s "https://masnavi.ai/api/verify?text=بشنو+این+نی"
```

Output: Verification result (exact/fuzzy/not_found).

## Notes
- API is public, no authentication required
- Rate limits are generous (public domain data)
- Corpus is updated regularly
- All content is in Persian (Farsi)
- Some commentary available in English
