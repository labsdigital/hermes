#!/bin/bash
# Max AI Daily Radar Script
# Runs daily at 06:00 WIB to curate AI signal and practical news

cd /opt/data/hermes

DATE=$(date +%Y-%m-%d)
WIB_DATE=$(TZ=Asia/Jakarta date +%Y-%m-%d)
OUTPUT_FILE="max/daily-brief/daily-brief-${WIB_DATE}.md"

echo "# 📡 AI Daily Radar - ${WIB_DATE}" > "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "*Radar Wilayah: Kurasi Filosofis & Praktis untuk Master Tamim*" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Section 1: Signal Finder (7 Regions)
echo "## 🔍 SIGNAL: Temuan Kritis Hari Ini" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Search for AI ethics, cognition, and socio-technical issues
echo '### Region Scan Results' >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"
echo '> *Note: Manual curation required for each day based on latest news*' >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"
echo '**Wilayah Monitoring:**' >> "$OUTPUT_FILE"
echo '- Mind: Atrofi kognitif, outsourcing memori' >> "$OUTPUT_FILE"
echo '- Heart: Chatbot empati, manipulasi afektif' >> "$OUTPUT_FILE"
echo '- Relationship: AI mediator, isolasi sosial' >> "$OUTPUT_FILE"
echo '- Culture: Bias dataset, kolonialisme epistemik' >> "$OUTPUT_FILE"
echo '- Work & Creation: Kanibalisme digital' >> "$OUTPUT_FILE"
echo '- Truth & Power: Kontrol algoritma, distorsi realitas' >> "$OUTPUT_FILE"
echo '- Meaning: Batas eksistensial, makna palsu' >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"

# Section 2: Practical News
echo "## 🛠️ PRAKTIS: Fitur & Tools Baru" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '**Pencarian Hari Ini:**' >> "$OUTPUT_FILE"
echo '- Gemini/NotebookLM updates' >> "$OUTPUT_FILE"
echo '- AI tools untuk pembelajaran' >> "$OUTPUT_FILE"
echo '- Aplikasi AI untuk media sosial' >> "$OUTPUT_FILE"
echo '- Tools produktivitas harian' >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"
echo 'Status: Menunggu input manual dari kurator'
echo '' >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"

# Section 3: Actionable Ideas
echo "## 💡 IDE ARTIKEL MINGGU INI" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo '*Tempat untuk ide provokatif berdasarkan signal hari ini*' >> "$OUTPUT_FILE"
echo '' >> "$OUTPUT_FILE"

# Git operations
git add "$OUTPUT_FILE"
git commit -m "Max: Daily Brief ${WIB_DATE}" 2>/dev/null || echo "No changes to commit"
git push origin main 2>/dev/null || echo "Push skipped"

echo "✅ Daily Radar completed for ${WIB_DATE}"
