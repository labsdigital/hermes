# Chalbi - Portal Rumi & Masnavi

Chalbi adalah subagent yang mengkhususkan diri dalam karya-karya **Jalaludin Rumi** (Mawlana), khususnya *Masnavi-ye Ma'navi* dan *Divan-e Shams*.

## 📚 Sumber Data

Chalbi terhubung langsung ke **masnavi.ai** - server MCP publik yang berisi:

### Masnavi-ye Ma'navi
- **25,635 beyt** (kuplet)
- **6 daftar** (buku)
- **972 section** (cerita/named sections)
- Sumber: Ganjoor.net (domain publik)

### Divan-e Shams
- **3,230 ghazal**
- **34,603 beyt**
- Puisi-puisi cinta dan mistisisme

## 🎯 Cara Kerja

### CLI Tool
```bash
cd /opt/data/hermes/chalbi
chmod +x scripts/chalbi.sh
./scripts/chalbi.sh meaning "cinta" 5
./scripts/chalbi.sh lookup M1:1
./scripts/chalbi.sh search عشق 10
./scripts/chalbi.sh verify "بشنو این نی"
./scripts/chalbi.sh random 1
./scripts/chalbi.sh toc 1
```

### API Endpoints
| Endpoint | Deskripsi |
|----------|-----------|
| `/api/search` | Full-text search (Persian) |
| `/api/search_meaning` | Semantic search (any language) |
| `/api/lookup` | Ambil beyt spesifik |
| `/api/verify` | Verifikasi keaslian kutipan |
| `/api/get_section` | Section lengkap |
| `/api/random_beyt` | Random beyt |
| `/api/table_of_contents` | Daftar section |

### Citation Format
- Masnavi: `M{daftar}:{beyt}` → contoh: `M1:1`
- Divan: `G{ghazal}:{beyt}` → contoh: `G1393:1`
- Global: `g:{n}` → contoh: `g:1`

## 📝 Output Format

Chalbi menghasilkan artikel dengan struktur:

```markdown
# [Judul Tema]

## Kutipan Rumi

> [Ayat Persia]
> — M{daftar}:{beyt}

### Terjemahan
[Bahasa Indonesia]

### Makna & Konteks
[Penjelasan filosofis Sufi]
```

## 🌟 Fitur Utama

- ✅ **Verifikasi Otentik** - Tidak ada kutipan palsu
- ✅ **Multi-bahasa** - Support search dalam bahasa apa pun
- ✅ **Konteks Filosofis** - Penjelasan mendalam
- ✅ **Source Tracing** - Semua kutipan dapat dilacak
- ✅ **Bulk Download** - Corpus lengkap tersedia

## 📖 Contoh Topik

- Cinta Ilahi (عشق)
- Perjalanan Spiritual
- Mati Sebelum Mati
- Cinta dan Kerinduann
- Tuhan dan Kehamilan
- Hewan dan Kebijaksanaan
- Musik dan Tari (Sama)
- Guru dan Murid

## 🔗 Links Penting

- **Website**: https://masnavi.ai/
- **Docs**: https://masnavi.ai/docs
- **LLMs.txt**: https://masnavi.ai/llms.txt
- **MCP Config**: https://masnavi.ai/.well-known/mcp.json
- **Corpus**: https://masnavi.ai/corpus.jsonl
- **API Spec**: https://masnavi.ai/api/openapi.json

## 📁 Struktur Repository

```
hermes/chalbi/
├── AGENTS.md              # Profil subagent
├── README.md              # File ini
├── scripts/
│   └── chalbi.sh          # CLI wrapper
├── reports/               # Output artikel
│   └── *.md
└── skills/
    └── rumi-masnavi/
        └── SKILL.md       # Skill definition
```

## 🚀 Cara Menggunakan @chalbi

1. **Tanya kutipan**: "@chalbi apa kata Rumi tentang cinta?"
2. **Verifikasi**: "@chalbi apakah kutipan ini asli?"
3. **Eksplorasi**: "@chalbi cari tema tentang Tuhan"
4. **Random**: "@chalbi beri saya beyt random dari Daftar 1"

Semua query akan terhubung ke API masnavi.ai dan menghasilkan konten yang dapat dipertanggungjawabkan.

---

*Dibuat oleh Hermes Agent untuk labsdigital/hermes*  
*Sumber: Jalal al-Din Rumi (1207-1273)*
