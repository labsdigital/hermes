#!/bin/bash
# Script untuk Chalbi: commit, push, dan upload ke FTP
# Usage: ./commit_article.sh <judul_file> [--email] [--ftp]

cd /opt/data/hermes

# Default: upload to FTP
UPLOAD_FTP=true

# Cek flag
if [ "${2}" = "--no-ftp" ] || [ "${3}" = "--no-ftp" ]; then
    UPLOAD_FTP=false
fi

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
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
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

# Upload ke FTP - show direct link
if [ "$UPLOAD_FTP" = true ]; then
    echo ""
    echo "📤 Mengupload ke FTP..."
    URL=$(python3 /opt/data/hermes/shared/ftp_upload.py "$FILE" "/chalbi/" 2>&1 | grep "✅ Uploaded:" | head -1)
    if [ -n "$URL" ]; then
        echo ""
        echo "🔗 Konten tersedia di: $URL"
    else
        # Fallback
        filename=$(basename "$FILE")
        echo ""
        echo "🔗 Konten tersedia di: https://ftp.rumahguru.org/chalbi/$filename"
    fi
fi

echo ""
echo "🎉 Workflow selesai!"
