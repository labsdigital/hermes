#!/bin/bash
# Script untuk Chalbi: commit dan push artikel ke GitHub + kirim email
# Usage: ./commit_article.sh <judul_file>
#        ./commit_article.sh <judul_file> --email

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

# Commit dengan pesan deskriptif
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
MESSAGE="Chalbi: ${1%.md}"
git commit -m "$MESSAGE"

# Push ke GitHub
git pull origin main --allow-unrelated-histories 2>/dev/null || true
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Berhasil push ke GitHub"
    echo "📄 File: $FILE"
    echo "🔗 URL: https://github.com/labsdigital/hermes/tree/main/chalbi/reports"
else
    echo "❌ Gagal push ke GitHub"
    exit 1
fi

# Kirim email jika diminta
if [ "${2}" = "--email" ] || [ "${3}" = "--email" ]; then
    echo ""
    echo "📧 Mengirim email..."
    python3 /opt/data/hermes/chalbi/scripts/send_email.py \
        --article "$FILE" \
        --recipient "tamimnasa.chalbi@blogger.com"
fi

echo ""
echo "🎉 Workflow selesai!"
