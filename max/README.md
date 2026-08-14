# Max - AI News Researcher & Writer

Subagent khusus untuk mencari informasi dan menulis artikel tentang kecerdasan buatan dalam Bahasa Indonesia.

## Fitur
- Riset berita AI dari sumber terpercaya
- Ringkasan dalam Bahasa Indonesia
- Artikel markdown yang mudah dibaca
- Publish otomatis ke folder reports/

## Struktur
```
hermes/max/
├── AGENTS.md          # Profil dan cara kerja Max
├── SKILL.md           # Petunjuk penggunaan skill
├── skills/
│   └── research-writer/
│       └── SKILL.md   # Skill utama Max
└── reports/           # Folder output artikel
```

## Cara Kerja
1. User memberikan topik atau instruksi
2. Max melakukan riset dari sumber online
3. Hasil riset diringkas dalam Bahasa Indonesia
4. Artikel ditulis dan disimpan di reports/
5. Max melaporkan hasil ke user

## Contoh Perintah
- "Cari info tentang OpenAI terbaru"
- "Buat artikel tentang perkembangan AI di Indonesia"
- "Riset news AI minggu ini"
- "Tulis tentang model bahasa terbaru"