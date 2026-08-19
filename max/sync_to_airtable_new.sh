#!/bin/bash
# Script untuk sync artikel ke Airtable - Table Baru (tblArticles)
# Usage: ./sync_to_airtable.sh <filename>
# 
# Struktur Table Baru:
# - id: Text (max-article-YYYY-MM-DD)
# - title: Text (judul terpisah!)
# - content: Long Text (full markdown)
# - published_at: Date (YYYY-MM-DD)

AIRTABLE_TOKEN="${AIRTABLE_API_KEY}"
if [ -z "$AIRTABLE_TOKEN" ]; then
    echo "❌ AIRTABLE_API_KEY tidak ditemukan di environment"
    exit 1
fi

ARTICLE_FILE="/opt/data/hermes/max/reports/${1}"
if [ ! -f "$ARTICLE_FILE" ]; then
    echo "❌ File tidak ditemukan: $ARTICLE_FILE"
    exit 1
fi

# Extract ID dari filename
FILENAME=$(basename "$ARTICLE_FILE" .md)
ARTICLE_ID="max-${FILENAME}"

# Extract date dari filename
DATE=$(echo "$FILENAME" | grep -oP '\d{4}-\d{2}-\d{2}' || date +%Y-%m-%d)

# Extract TITLE dari line pertama markdown (hapus # dan spasi)
TITLE=$(head -1 "$ARTICLE_FILE" | sed 's/^# //')

# Read content
CONTENT=$(cat "$ARTICLE_FILE")

echo "📊 Syncing ke Airtable..."
echo "   ID: $ARTICLE_ID"
echo "   Title: $TITLE"
echo "   Date: $DATE"

# Encode content sebagai JSON string
CONTENT_JSON=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$CONTENT")
TITLE_JSON=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$TITLE")

# Target table - GANTI TABLE_ID sesuai tabel baru yang dibuat
TABLE_ID="tblExdQkNbL9bZbgQ"
BASE_ID="${AIRTABLE_BASE_ID:-appHDwcERrnRH02YS}"

# Kirim ke Airtable dengan field title
RESPONSE=$(curl -s -X POST "https://api.airtable.com/v0/${BASE_ID}/${TABLE_ID}" \
    -H "Authorization: Bearer ${AIRTABLE_TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"records\":[{\"fields\":{\"id\":\"${ARTICLE_ID}\",\"title\":${TITLE_JSON},\"content\":${CONTENT_JSON},\"published_at\":\"${DATE}\"}}]}")

# Check response
if echo "$RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); exit(0 if 'records' in d else 1)" 2>/dev/null; then
    RECORD_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['records'][0]['id'])")
    echo "✅ Berhasil! Record ID: $RECORD_ID"
    exit 0
else
    echo "❌ Gagal!"
    echo "Response: $RESPONSE"
    exit 1
fi
