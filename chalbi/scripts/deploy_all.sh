#!/bin/bash
# Batch upload all Chalbi articles to hosting
# Usage: ./deploy_all.sh

cd /opt/data/hermes

# CONFIGURATION
FTP_HOST="ftp.rumahguru.org"
FTP_USER="hermes@taraka.id"
FTP_PASS="H32m35."
FTP_PORT="21"
REMOTE_PATH="/public_html/chalbi/"

# Check if lftp is available
if ! command -v lftp &> /dev/null; then
    echo "❌ lftp is not installed. Please install it first."
    exit 1
fi

echo "🚀 Deploying Chalbi articles to hosting..."
echo "   Host: $FTP_HOST:$FTP_PORT"
echo "   Path: $REMOTE_PATH"
echo ""

# Create lftp script
LFTP_SCRIPT=$(mktemp)
cat > "$LFTP_SCRIPT" << EOF
set ftp:ssl-allow no
set ssl:verify-certificate no
open -p $FTP_PORT -u $FTP_USER,$FTP_PASS $FTP_HOST
cd $REMOTE_PATH
mkdir -p scripts
EOF

# Upload all MD and HTML files
echo "📄 Uploading Markdown articles..."
for file in chalbi/reports/*.md; do
    if [ -f "$file" ]; then
        echo "upload \"$file\";" >> "$LFTP_SCRIPT"
    fi
done

echo "🎨 Uploading HTML previews..."
for file in chalbi/reports/*.html; do
    if [ -f "$file" ]; then
        echo "upload \"$file\";" >> "$LFTP_SCRIPT"
    fi
done

echo "📁 Uploading scripts..."
for file in chalbi/scripts/*.sh; do
    if [ -f "$file" ]; then
        echo "upload \"$file\" \"scripts/\";" >> "$LFTP_SCRIPT"
    fi
done

echo "bye;" >> "$LFTP_SCRIPT"

# Execute upload
lftp -f "$LFTP_SCRIPT"
RESULT=$?

# Cleanup
rm -f "$LFTP_SCRIPT"

if [ $RESULT -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "📰 Articles available at:"
    for file in chalbi/reports/*.md; do
        if [ -f "$file" ]; then
            title=$(basename "$file" .md)
            echo "   • $title → https://$FTP_HOST${REMOTE_PATH}${title}.html"
        fi
    done
else
    echo ""
    echo "❌ Deployment failed"
    exit 1
fi
