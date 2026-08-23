#!/bin/bash
# Script untuk sync artikel ke Airtable
# Usage: ./sync_to_airtable.sh <filename>

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
DATETIME=$(date -d "$DATE" +"%Y-%m-%dT%H:%M:%S.000Z" 2>/dev/null || echo "2026-08-19T00:00:00.000Z")

echo "📊 Syncing ke Airtable..."
echo "   ID: $ARTICLE_ID"
echo "   Date: $DATE"

# Read content dan encode sebagai JSON
CONTENT=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" < "$ARTICLE_FILE")

# Kirim ke Airtable dengan field published_at
RESPONSE=$(curl -s -X POST "https://api.airtable.com/v0/appHDwcERrnRH02YS/tblExdQkNbL9bZbgQ" \
    -H "Authorization: Bearer $AIRTABLE_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"records\":[{\"fields\":{\"id\":\"$ARTICLE_ID\",\"content\":$CONTENT,\"published_at\":\"$DATETIME\"}}]}")

# Check response
if echo "$RESPONSE" | grep -q '"id"'; then
    RECORD_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['records'][0]['id'])")
    echo "✅ Berhasil! Record ID: $RECORD_ID"
else
    # Jika error UNKNOWN_FIELD_NAME, field belum dibuat
    if echo "$RESPONSE" | grep -q 'UNKNOWN_FIELD_NAME'; then
        echo "⚠️  Field 'published_at' belum dibuat di Airtable"
        echo "   Silakan buat field 'published_at' tipe DateTime di Airtable UI"
        echo "   Setelah itu jalankan ulang script ini"
        
        # Coba tanpa published_at
        RESPONSE=$(curl -s -X POST "https://api.airtable.com/v0/appHDwcERrnRH02YS/tblExdQkNbL9bZbgQ" \
            -H "Authorization: Bearer $AIRTABLE_TOKEN" \
            -H "Content-Type: application/json" \
            -d "{\"records\":[{\"fields\":{\"id\":\"$ARTICLE_ID\",\"content\":$CONTENT}}]}")
        
        if echo "$RESPONSE" | grep -q '"id"'; then
            RECORD_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['records'][0]['id'])")
            echo "✅ Tersimpan tanpa tanggal (field belum tersedia)"
            echo "   Record ID: $RECORD_ID"
        else
            echo "❌ Sync gagal:"
            echo "$RESPONSE"
            exit 1
        fi
    else
        echo "⚠️  Sync gagal:"
        echo "$RESPONSE"
        exit 1
    fi
fi
