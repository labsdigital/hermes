#!/bin/bash
# Atlas Essay Commit & Publish Script
# Usage: bash atlas/scripts/commit_essay.sh <filename.md> [--email]

set -e

cd /opt/data/hermes

# Check if file exists
FILE="atlas/reports/${1}"
if [ ! -f "$FILE" ]; then
    echo "❌ Error: File not found: $FILE"
    exit 1
fi

echo "📝 Processing: $FILE"

# Git operations
git add "$FILE" atlas/ shared/
git commit -m "Atlas: ${1%.md}"
git pull origin main --allow-unrelated-histories 2>/dev/null || true
git push origin main

echo "✅ Committed and pushed to GitHub"

# Email if requested
if [ "${2}" = "--email" ] || [ "${3}" = "--email" ]; then
    echo "📧 Sending email..."
    python3 /opt/data/hermes/atlas/scripts/send_email.py --article "$FILE"
fi

# FTP Upload
echo ""
echo "📤 Uploading to FTP..."
FILENAME=$(basename "$FILE")
python3 /opt/data/hermes/shared/ftp_upload.py "$FILE" "/atlas/" >/dev/null 2>&1

echo ""
echo "🔗 https://ftp.rumahguru.org/atlas/$FILENAME"
echo ""
echo "🎉 Done!"
