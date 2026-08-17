#!/bin/bash
# Max AI News Workflow - Generate, push to GitHub, Airtable & Email
# This script should be run from /opt/data/hermes

set -e

TIMESTAMP=$(date +%Y-%m-%d)
NEWS_FILE="ai_news_summary_$TIMESTAMP.md"

echo "🤖 Max AI News Workflow"
echo "📅 $TIMESTAMP $(date +%H:%M)"
echo ""

# Step 1: Generate news from RSS
echo "📡 Step 1: Mengambil berita AI terbaru dari RSS feeds..."
cd /opt/data
python3 /opt/data/home/.hermes/scripts/generate_github_news.py 2>/dev/null > "$NEWS_FILE"

if [ ! -f "$NEWS_FILE" ]; then
    echo "❌ Failed to generate news"
    exit 1
fi

echo "✅ News generated: $NEWS_FILE"
echo ""

# Step 2: Copy to Max reports
echo "📝 Step 2: Copying to Max reports..."
cp "$NEWS_FILE" /opt/data/hermes/max/reports/
echo "✅ Copied to: max/reports/$NEWS_FILE"
echo ""

# Step 3: Push to GitHub
echo "🚀 Step 3: Pushing to GitHub..."
cd /opt/data/hermes
git add max/reports/"$NEWS_FILE" .gitignore 2>/dev/null || true

if git diff --cached --quiet; then
    echo "   (No changes to commit)"
else
    git commit -m "Max: AI News Summary $TIMESTAMP"
    git pull origin main --allow-unrelated-histories 2>/dev/null || true
    git push origin main 2>/dev/null
    echo "✅ Pushed to GitHub"
fi
echo ""

# Step 4: Sync to Airtable (optional)
if [ -n "$AIRTABLE_API_KEY" ]; then
    echo "📊 Step 4: Syncing to Airtable..."
    python3 << PYEOF
import json, urllib.request, os

news_file = "$NEWS_FILE"
base_id = "$BASE_ID"
table_id = "$TABLE_ID"
article_id = "max-$TIMESTAMP"
token = os.environ.get("AIRTABLE_API_KEY", "")

with open(news_file, "r") as f:
    content = f.read()

data = {"records": [{"fields": {"id": article_id, "content": content}}]}
payload = json.dumps(data).encode()

req = urllib.request.Request(
    f"https://api.airtable.com/v0/{base_id}/{table_id}",
    data=payload,
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST"
)

try:
    resp = urllib.request.urlopen(req).read()
    print("✅ Synced to Airtable")
except Exception as e:
    print(f"⚠️  Airtable sync failed: {e}")
PYEOF
fi
echo ""

# Step 5: Send email notification
echo "📧 Step 5: Sending email notification..."
python3 /opt/data/hermes/max/send_email.py --article "/opt/data/hermes/max/reports/$NEWS_FILE" --recipient "tamimnasa@gmail.com" 2>&1 || echo "⚠️  Email send failed"
echo ""

echo "🎉 Workflow complete!"
echo "   GitHub: https://github.com/labsdigital/hermes/tree/main/max/reports"
echo "   Airtable: https://airtable.com/appHDwcERrnRH02YS/tbl9TvJ9QztbHeyaY"
