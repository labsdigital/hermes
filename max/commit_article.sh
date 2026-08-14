#!/bin/bash
# Script untuk Max: commit dan push artikel ke GitHub
# Usage: ./commit_max_article.sh <judul_file>

cd /opt/data/hermes

# Cek file yang akan di-commit
FILE="max/reports/${1}"
if [ ! -f "$FILE" ]; then
    echo "Error: File tidak ditemukan: $FILE"
    exit 1
fi

# Tambah file ke git
git add "$FILE"
git add max/

# Commit dengan pesan deskriptif
TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
MESSAGE="Max: Artikel tentang ${1%.md}"
git commit -m "$MESSAGE"

# Push ke GitHub
git push origin main

if [ $? -eq 0 ]; then
    echo "✅ Berhasil push ke GitHub"
    echo "📄 File: $FILE"
    echo "🔗 URL: https://github.com/labsdigital/hermes/tree/main/max/reports"
else
    echo "❌ Gagal push ke GitHub"
    exit 1
fi
