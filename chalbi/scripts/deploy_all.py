#!/usr/bin/env python3
"""
Batch upload all Chalbi articles to hosting via FTP
Usage: python3 deploy_all.py
"""

import ftplib
import sys
from pathlib import Path

# CONFIGURATION
FTP_HOST = "ftp.rumahguru.org"
FTP_USER = "hermesftp@taraka.id"
FTP_PASS = "H32m35."
FTP_PORT = 21
REMOTE_PATH = "/chalbi/"

def deploy_all():
    """Upload all articles and scripts to FTP"""
    try:
        # Connect
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.encoding = "utf-8"
        
        print("🚀 Deploying Chalbi articles to hosting...")
        print(f"   Host: {FTP_HOST}")
        print(f"   Path: {REMOTE_PATH}")
        print("")
        
        # Ensure directory exists
        try:
            ftp.cwd(REMOTE_PATH)
        except:
            print(f"📁 Creating directory: {REMOTE_PATH}")
            ftp.mkd(REMOTE_PATH.strip('/'))
            ftp.cwd(REMOTE_PATH)
        
        # Upload MD files
        print("📄 Uploading Markdown articles...")
        md_files = list(Path("chalbi/reports").glob("*.md"))
        for f in md_files:
            print(f"   - {f.name}")
            with open(f, 'rb') as fp:
                ftp.storbinary(f'STOR {f.name}', fp)
        print(f"   ✅ {len(md_files)} files uploaded")
        print("")
        
        # Upload HTML files
        print("🎨 Uploading HTML previews...")
        html_files = list(Path("chalbi/reports").glob("*.html"))
        for f in html_files:
            print(f"   - {f.name}")
            with open(f, 'rb') as fp:
                ftp.storbinary(f'STOR {f.name}', fp)
        print(f"   ✅ {len(html_files)} files uploaded")
        print("")
        
        # Upload scripts
        print("📁 Uploading scripts...")
        script_files = list(Path("chalbi/scripts").glob("*.py"))
        for f in script_files:
            print(f"   - {f.name}")
            with open(f, 'rb') as fp:
                ftp.storbinary(f'STOR {f.name}', fp)
        print(f"   ✅ {len(script_files)} scripts uploaded")
        print("")
        
        # Verify
        print("📋 Verification...")
        ftp.cwd(REMOTE_PATH)
        files = ftp.nlst()
        print(f"   Total files: {len(files)}")
        for f in sorted(files):
            print(f"   - {f}")
        
        ftp.quit()
        
        print("")
        print("✅ Deployment successful!")
        print(f"🌐 Articles: https://ftp.rumahguru.org{REMOTE_PATH}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = deploy_all()
    sys.exit(0 if success else 1)