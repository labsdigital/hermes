#!/bin/bash
# Upload files to hosting via FTP
# Usage: ./upload_to_hosting.sh <file_or_folder> [remote_path]

# CONFIGURATION
FTP_HOST="ftp.rumahguru.org"
FTP_USER="hermes@taraka.id"
FTP_PASS="H32m35."
FTP_PORT="21"
REMOTE_PATH="/public_html/chalbi/"

# Check if lftp is available
if ! command -v lftp &> /dev/null; then
    echo "❌ lftp is not installed. Install with: sudo apt-get install lftp"
    exit 1
fi

# Check arguments
if [ -z "$1" ]; then
    echo "Usage: $0 <file_or_folder> [remote_path]"
    echo ""
    echo "Examples:"
    echo "  $0 index.html"
    echo "  $0 chalbi/reports/"
    echo "  $0 article.md /articles/"
    exit 1
fi

SOURCE="$1"
DEST="${2:-$REMOTE_PATH}"

# Convert relative path to absolute
if [[ "$SOURCE" != /* ]]; then
    SOURCE="$(pwd)/$SOURCE"
fi

if [ ! -e "$SOURCE" ]; then
    echo "❌ Source not found: $SOURCE"
    exit 1
fi

echo "📤 Uploading to FTP..."
echo "   Source: $SOURCE"
echo "   Host: $FTP_HOST:$FTP_PORT"
echo "   User: $FTP_USER"
echo "   Destination: $DEST"
echo ""

# Create lftp script
LFTP_SCRIPT=$(mktemp)
cat > "$LFTP_SCRIPT" << EOF
set ftp:ssl-allow no
set ssl:verify-certificate no
open -p $FTP_PORT -u $FTP_USER,$FTP_PASS $FTP_HOST
cd $DEST
EOF

# If source is a file
if [ -f "$SOURCE" ]; then
    echo "upload \"$SOURCE\";" >> "$LFTP_SCRIPT"
elif [ -d "$SOURCE" ]; then
    echo "mirror -R \"$SOURCE\"/ ." >> "$LFTP_SCRIPT"
fi

echo "bye;" >> "$LFTP_SCRIPT"

# Execute upload
lftp -f "$LFTP_SCRIPT"
RESULT=$?

# Cleanup
rm -f "$LFTP_SCRIPT"

if [ $RESULT -eq 0 ]; then
    echo ""
    echo "✅ Upload successful!"
    if [ -f "$SOURCE" ]; then
        echo "   URL: https://$FTP_HOST${DEST%/}/$(basename "$SOURCE")"
    else
        echo "   URL: https://$FTP_HOST${DEST%/}/"
    fi
else
    echo ""
    echo "❌ Upload failed"
    exit 1
fi
