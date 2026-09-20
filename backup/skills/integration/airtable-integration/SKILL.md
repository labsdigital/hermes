---
name: airtable-integration
category: integration
description: Airtable API patterns for article storage sync.
---

# Airtable Integration Patterns

Integrasi aplikasi dengan Airtable API untuk storage dan retrieval data.

## Critical Limitations

**Field Creation via API Blocked**: Airtable API does NOT allow creating/modifying table schemas (fields) programmatically. Must be done manually via UI.

Error you'll see: `UNKNOWN_FIELD_NAME` when trying to write to non-existent field.

## Workflow Pattern

```
1. Create table via Airtable UI
   → Add fields manually (id, title, content, published_at)
   
2. Get Table ID from URL
   → Format: https://airtable.com/appXXXXXX/tblYYYYYY
   → Copy: tblYYYYYY
   
3. Configure application
   → Set AIRTABLE_TABLE_ID environment variable
   → Use correct Base ID and Table ID
   
4. Test connection
   → GET /v0/{baseId}/{tableId}?maxRecords=1
   
5. Sync data
   → POST /v0/{baseId}/{tableId} with records array
```

## Common Fields Structure (Article Storage)

| Field | Type | Purpose |
|-------|------|---------|
| id | Text | Unique identifier (max-article-YYYY-MM-DD) |
| title | Single line text | Article title (SEPARATE from content) |
| content | Long text | Full markdown content |
| published_at | Date | Publication date for sorting |

## API Endpoints

### Read Records
```bash
GET https://api.airtable.com/v0/{baseId}/{tableId}
Headers: Authorization: Bearer {token}
Query: ?maxRecords=50&sort[]=fieldName&sort[0]=published_at&sort[1]=desc
```

### Create Records
```bash
POST https://api.airtable.com/v0/{baseId}/{tableId}
Headers: Authorization: Bearer {token}, Content-Type: application/json
Body: {"records": [{"fields": {"id": "...", "title": "...", "content": "...", "published_at": "2026-08-19"}}]}
```

### Update Records
```bash
PATCH https://api.airtable.com/v0/{baseId}/{tableId}
Body: {"records": [{"id": "recXXX", "fields": {"published_at": "2026-08-19"}}]}
```

## Getting Table ID

1. Open table in Airtable UI
2. Look at URL: `https://airtable.com/{baseId}/tbl{tableId}`
3. Copy the `tbl{tableId}` portion
4. Format: 22 characters, starts with "tbl"

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `UNKNOWN_FIELD_NAME` | Field doesn't exist | Create field via UI first |
| `AUTHENTICATION_REQUIRED` | Invalid/expired token | Regenerate API token |
| `NOT_FOUND` | Wrong base/table ID | Verify IDs from UI |
| `INVALID_PERMISSIONS` | Token lacks access | Check token permissions |

## PHP Example

```php
// Configuration
$AIRTABLE_API_KEY = getenv('AIRTABLE_API_KEY');
$AIRTABLE_BASE_ID = 'appHDwcERrnRH02YS';
$AIRTABLE_TABLE_ID = 'tblExdQkNbL9bZbgQ';

// Fetch with sort
$url = "https://api.airtable.com/v0/{$AIRTABLE_BASE_ID}/{$AIRTABLE_TABLE_ID}"
     . "?maxRecords=50"
     . "&sort[]=fieldName&sort[0]=published_at&sort[1]=desc";

// Sort fallback (if published_at not available)
usort($records, function($a, $b) {
    $dateA = $a['fields']['published_at'] ?? extractDateFromId($a['fields']['id']);
    $dateB = $b['fields']['published_at'] ?? extractDateFromId($b['fields']['id']);
    return strtotime($dateB) - strtotime($dateA);
});
```

## Bash Sync Script Pattern

```bash
#!/bin/bash
# Extract title from markdown first line
TITLE=$(head -1 "$ARTICLE_FILE" | sed 's/^# //')

# Extract date from filename
DATE=$(echo "$FILENAME" | grep -oP '\d{4}-\d{2}-\d{2}')

# Encode as JSON
TITLE_JSON=$(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$TITLE")

# POST to Airtable
curl -s -X POST "https://api.airtable.com/v0/${BASE_ID}/${TABLE_ID}" \
  -H "Authorization: Bearer ${AIRTABLE_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"records\":[{\"fields\":{\"id\":\"${ARTICLE_ID}\",\"title\":${TITLE_JSON},\"content\":${CONTENT_JSON},\"published_at\":\"${DATE}\"}}]}"
```

## Related Files

- `/opt/data/hermes/max/sync_to_airtable_new.sh` - Sync script for new table structure
- `/opt/data/hermes/max/index_new.php` - PHP blog reader for new table
- `/opt/data/.env` - Contains AIRTABLE_API_KEY