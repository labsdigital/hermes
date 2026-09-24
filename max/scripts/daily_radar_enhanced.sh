#!/bin/bash
# Max AI Daily Radar - Enhanced Version
# Searches for AI news and curates based on 7 Regions framework

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

# Section 1: Signal Finder
echo "## 🔍 SIGNAL: Temuan Kritis Hari Ini" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "*Mencari berita AI yang berdampak pada 7 Wilayah Kemanusiaan...*" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Search queries for different regions
echo "### Pencarian Signal" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "- Mind: AI cognition, memory outsourcing, learning changes" >> "$OUTPUT_FILE"
echo "- Heart: AI empathy, chatbot therapy, emotional manipulation" >> "$OUTPUT_FILE"
echo "- Relationship: AI mediation, social isolation" >> "$OUTPUT_FILE"
echo "- Culture: Dataset bias, epistemic colonialism" >> "$OUTPUT_FILE"
echo "- Work: Digital cannibalism, creativity devaluation" >> "$OUTPUT_FILE"
echo "- Truth: Algorithm control, reality distortion" >> "$OUTPUT_FILE"
echo "- Meaning: Existential boundaries, false meaning" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Section 2: Practical News
echo "## 🛠️ PRAKTIS: Fitur & Tools Baru" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "*Mencari tool AI praktis untuk pembelajaran dan produktivitas...*" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "- Gemini/NotebookLM updates" >> "$OUTPUT_FILE"
echo "- AI tools untuk siswa" >> "$OUTPUT_FILE"
echo "- Tools media sosial" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Section 3: Article Ideas
echo "## 💡 IDE ARTIKEL MINGGU INI" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"
echo "*Ide provokatif berdasarkan signal hari ini*" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Git operations
git add "$OUTPUT_FILE"
git commit -m "Max: Daily Brief ${WIB_DATE}" 2>/dev/null || echo "No changes to commit"
git push origin main 2>/dev/null || echo "Push skipped"

echo "✅ Daily Radar completed for ${WIB_DATE}"
echo "📄 Output: ${OUTPUT_FILE}"
