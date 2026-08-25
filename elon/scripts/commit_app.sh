#!/bin/bash
# Script untuk Elon: commit, push, dan upload ke FTP
# Usage: ./commit_app.sh <folder_name> [--email]

cd /opt/data/hermes

FOLDER="elon/${1}"
if [ ! -d "$FOLDER" ]; then
    echo "Error: Folder tidak ditemukan: $FOLDER"
    exit 1
fi

# Find index.html
HTML_FILE=$(find "$FOLDER" -name "index.html" | head -1)
if [ -z "$HTML_FILE" ]; then
    echo "Error: Tidak ada index.html di $FOLDER"
    exit 1
fi

git add "$FOLDER" elon/ shared/
git commit -m "Elon: ${1}"
git pull origin main --allow-unrelated-histories 2>/dev/null || true
git push origin main

if [ "${2}" = "--email" ] || [ "${3}" = "--email" ]; then
    echo ""
    echo "📧 Mengirim email..."
fi

echo ""
echo "📤 Mengupload ke FTP..."
python3 /opt/data/hermes/shared/ftp_upload_folder.py "$FOLDER" "/elon/$1/" >/dev/null 2>&1

echo ""
echo "🔗 https://ftp.rumahguru.org/elon/$1/"
echo ""
echo "🎉 Workflow selesai!"
