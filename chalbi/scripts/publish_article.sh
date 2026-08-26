#!/bin/bash
# Chalbi Article Publish Workflow
# Order: GitHub commit → get URLs → FTP upload → email
# Usage: ./publish_article.sh <filename> [--email]

set -e

cd /opt/data/hermes

FILE="chalbi/reports/${1}"
if [ ! -f "$FILE" ]; then
    echo "❌ File tidak ditemukan: $FILE"
    exit 1
fi

REPO_URL="https://github.com/labsdigital/hermes"
BRANCH="main"

# ── Step 1: Commit & Push to GitHub ──────────────────────────────
echo "📝 Committing to GitHub..."
git add "$FILE"
git add chalbi/
git add shared/

MESSAGE="Chalbi: ${1%.md}"
git commit -m "$MESSAGE"

git pull origin main --allow-unrelated-histories 2>/dev/null || true
git push origin main

if [ $? -ne 0 ]; then
    echo "❌ GitHub push failed!"
    exit 1
fi
echo "✅ GitHub push berhasil"

# ── Step 2: Get GitHub raw URLs for images ──────────────────────
echo ""
echo "🔗 Generating GitHub raw URLs..."

# Find all image references in the article (markdown format: ![alt](url))
# Replace taraka.id URLs with GitHub raw URLs
sed -i 's|https://taraka\.id/hermes/chalbi/\([^)]*\)\.png|https://raw.githubusercontent.com'"$REPO_URL"'/'"$BRANCH"'/chalbi/reports/\1.png|g' "$FILE"
sed -i 's|https://taraka\.id/hermes/chalbi/\([^)]*\)\.jpg|https://raw.githubusercontent.com'"$REPO_URL"'/'"$BRANCH"'/chalbi/reports/\1.jpg|g' "$FILE"
sed -i 's|https://taraka\.id/hermes/chalbi/\([^)]*\)\.svg|https://raw.githubusercontent.com'"$REPO_URL"'/'"$BRANCH"'/chalbi/reports/\1.svg|g' "$FILE"

echo "✅ Image URLs updated to GitHub raw"

# ── Step 3: Upload to FTP ───────────────────────────────────────
echo ""
echo "📤 Uploading to FTP..."
FILENAME=$(basename "$FILE")
python3 /opt/data/hermes/shared/ftp_upload.py "$FILE" "/chalbi/" >/dev/null 2>&1
echo "✅ FTP upload berhasil"

# ── Step 4: Send Email ──────────────────────────────────────────
if [ "${2}" = "--email" ] || [ "${3}" = "--email" ]; then
    echo ""
    echo "📧 Sending email..."
    python3 /opt/data/hermes/chalbi/scripts/send_email.py \
        --article "$FILE" \
        --recipient "tamimnasa.chalbi@blogger.com"
    echo "✅ Email terkirim"
fi

# ── Summary ─────────────────────────────────────────────────────
echo ""
echo "📰 Article URL (GitHub raw): https://raw.githubusercontent.com/${REPO_URL#https://}/${BRANCH}/${FILE}"
echo "🖼️  Image URLs updated to GitHub raw"
echo "🎉 Workflow selesai!"
