#!/bin/bash
cd /opt/data/hermes
FILE="max/reports/${1}"
if [ ! -f "$FILE" ]; then echo "Error: $FILE"; exit 1; fi
git add "$FILE" max/ shared/
git commit -m "Max: ${1%.md}"
git pull origin main --allow-unrelated-histories 2>/dev/null || true
git push origin main
if [ "${2}" = "--email" ] || [ "${3}" = "--email" ]; then
    python3 /opt/data/hermes/max/scripts/send_email.py --article "$FILE" 2>/dev/null || true
fi
echo ""
echo "📤 Uploading to FTP..."
FILENAME=$(basename "$FILE")
python3 /opt/data/hermes/shared/ftp_upload.py "$FILE" "/max/" >/dev/null 2>&1
echo ""
echo "🔗 https://ftp.rumahguru.org/max/$FILENAME"
echo ""
echo "🎉 Done!"
