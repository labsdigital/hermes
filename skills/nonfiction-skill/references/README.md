# Nonfiction Writing Skill (Atlas Style)

Skill lengkap untuk menulis esai non-fiksi dengan gaya Yuval Noah Harari, dilengkapi panduan pembuatan ilustrasi SVG dan gambar artistik.

## Fitur Utama

- **Struktur esai**: 5-8 bagian (Hook → Definisi → Eksplorasi → Refleksi → Implikasi → Penutup)
- **Teknik menulis**: Defamiliarization, Grand Synthesis, Paradoks, Metafora Visual
- **Anti-AI patterns**: Panduan humanisasi teks (integrasi dengan skill `humanizer`)
- **Ilustrasi SVG**: Template siap pakai untuk diagram konseptual
- **Gambar artistik**: Panduan penggunaan Pollinations AI (polli CLI)
- **Workflow publikasi**: GitHub-first → FTP → Email

## Struktur File

```
nonfiction-skill/
├── SKILL.md                    # Skill utama (writing + illustration guide)
└── references/
    ├── harari-style-guide.md   # Prinsip inti: defamiliarization, grand synthesis
    ├── writing-techniques.md   # Teknik detail: opening, closing, transitions
    ├── chapter-blueprints.md   # Template struktur: 6 blueprint untuk berbagai jenis
    ├── svg-templates.md        # Template SVG siap pakai
    └── README.md               # File ini
```

## Penggunaan

Skill ini dimuat otomatis oleh subagent Atlas saat membuat esai non-fiksi. Untuk manual loading:

```bash
skill_view(name='nonfiction-skill')
```

## Sumber Referensi

Skill ini menggabungkan dan mengadaptasi konten dari:

1. **nonfiction-harari-style** (taraka.id) — Prinsip dan teknik penulisan Harari
   - https://taraka.id/AGENTS/?path=skills/nonfiction-style
   
2. **svg-skill** (Hermes) — Panduan teknis pembuatan SVG
   - https://github.com/nousresearch/hermes-agent/tree/main/skills/svg-skill

3. **humanizer** (Hermes) — Anti-AI patterns untuk humanisasi teks
   - https://github.com/blader/humanizer

## Artikel Contoh

Artikel Atlas yang ditulis menggunakan skill ini:
- Mesin yang Perlu Diasuh (1.809 kata) — 2026-08-26
- Qualia (1.706 kata)
- Garis Demarkasi (1.744 kata)
- Otak yang Menyewakan Diri (1.937 kata)
- Mitos Augmentasi (2.166 kata)
- Dua Keturunan Terakhir (2.129 kata)

## Lisensi

MIT — bebas digunakan dan dimodifikasi.
