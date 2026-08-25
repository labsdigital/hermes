#!/bin/bash
# Script untuk Chalbi: commit, push, dan upload ke FTP
# Usage: ./commit_article.sh <judul_file> [--email]

cd /opt/data/hermes

# Cek file yang akan di-commit
FILE="chalbi/reports/${1}"
if [ ! -f "$FILE" ]; then
    echo "Error: File tidak ditemukan: $FILE"
    exit 1
fi

# Tambah file ke git
git add "$FILE"
git add chalbi/
git add shared/

# Commit dengan pesan deskriptif
MESSAGE="Chalbi: ${1%.md}"
git commit -m "$MESSAGE"

# Push ke GitHub
git pull origin main --allow-unrelated-histories 2>/dev/null || true
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Berhasil push ke GitHub"
else
    echo "⚠️  GitHub push failed, continuing with FTP..."
fi

# Kirim email jika diminta
if [ "${2}" = "--email" ] || [ "${3}" = "--email" ]; then
    echo ""
    echo "📧 Mengirim email..."
    python3 /opt/data/hermes/chalbi/scripts/send_email.py \
        --article "$FILE" \
        --recipient "tamimnasa.chalbi@blogger.com"
fi

# Upload ke FTP - show DIRECT content link
echo ""
echo "📤 Mengupload ke FTP..."
FILENAME=$(basename "$FILE")
URL="https://ftp.rumahguru.org/chalbi/$FILENAME"

python3 /opt/data/hermes/shared/ftp_upload.py "$FILE" "/chalbi/" >/dev/null 2>&1

echo ""
echo "🔗 $URL"
echo ""
echo "🎉 Workflow selesai!"
