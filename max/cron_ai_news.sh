#!/bin/bash
# Cron Job untuk Max: Generate berita AI + Sync ke GitHub & Airtable
# Jalankan: bash max/cron_ai_news.sh

set -e

cd /opt/data

echo "🤖 Max AI News Generator"
echo "📅 $(date '+%Y-%m-%d %H:%M')"
echo ""

# Load environment variables
if [ -f /opt/data/.env ]; then
    export $(grep -v '^#' /opt/data/.env | xargs)
fi

# Step 1: Generate berita AI dari RSS
echo "📡 Step 1: Mengambil berita AI terbaru..."
python3 /opt/data/home/.hermes/scripts/generate_github_news.py 2>/dev/null > /opt/data/ai_news_summary_$(date +%Y-%m-%d).md

if [ -f "/opt/data/ai_news_summary_$(date +%Y-%m-%d).md" ]; then
    echo "✅ Berita berhasil di-generate"
else
    echo "❌ Gagal generate berita"
    exit 1
fi

# Step 2: Copy ke Max reports dan push ke GitHub + Airtable
echo ""
echo "📝 Step 2: Memproses untuk Max..."
cp /opt/data/ai_news_summary_$(date +%Y-%m-%d).md /opt/data/hermes/max/reports/

cd /opt/data/hermes
bash max/commit_article.sh ai_news_summary_$(date +%Y-%m-%d).md

echo ""
echo "🎉 Workflow selesai!"
echo "   - GitHub: https://github.com/labsdigital/hermes/tree/main/max/reports"
echo "   - Airtable: https://airtable.com/appHDwcERrnRH02YS/tbl9TvJ9QztbHeyaY"
