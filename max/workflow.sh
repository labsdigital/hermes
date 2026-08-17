#!/bin/bash
# Max AI News Workflow - Generate, push to GitHub & Airtable
set -e
TIMESTAMP=$(date +%Y-%m-%d)
NEWS_FILE="ai_news_summary_$TIMESTAMP.md"
echo "🤖 Max AI News Workflow - $TIMESTAMP"
cd /opt/data
python3 /opt/data/home/.hermes/scripts/generate_github_news.py 2>/dev/null > "$NEWS_FILE"
cp "$NEWS_FILE" /opt/data/hermes/max/reports/
cd /opt/data/hermes
git add max/reports/"$NEWS_FILE" .gitignore 2>/dev/null || true
if ! git diff --cached --quiet; then
    git commit -m "Max: AI News Summary $TIMESTAMP"
    git pull origin main --allow-unrelated-histories 2>/dev/null || true
    git push origin main
fi
echo "✅ Pushed to GitHub"
echo "📄 https://github.com/labsdigital/hermes/tree/main/max/reports"
exit 0
