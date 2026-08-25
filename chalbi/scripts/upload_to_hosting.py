#!/usr/bin/env python3
"""
Upload file to hosting via FTP
Usage: python3 upload_to_hosting.py <file> [remote_path]
"""

import ftplib
import sys
from pathlib import Path

# CONFIGURATION
FTP_HOST = "ftp.rumahguru.org"
FTP_USER = "hermes@taraka.id"
FTP_PASS = "H32m35."
FTP_PORT = 21
REMOTE_PATH = "/chalbi/"

def upload_file(file_path, remote_path=None):
    """Upload a single file to FTP"""
    if remote_path is None:
        remote_path = REMOTE_PATH
    
    try:
        # Connect
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.encoding = "utf-8"
        
        # Ensure directory exists
        try:
            ftp.cwd(remote_path)
        except:
            ftp.mkd(remote_path.strip('/'))
            ftp.cwd(remote_path)
        
        # Upload
        filename = Path(file_path).name
        print(f"📤 Uploading: {filename}")
        with open(file_path, 'rb') as fp:
            ftp.storbinary(f'STOR {filename}', fp)
        
        ftp.quit()
        print(f"✅ Uploaded to: https://ftp.rumahguru.org{remote_path}{filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upload_to_hosting.py <file> [remote_path]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    remote = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)
    
    success = upload_file(file_path, remote)
    sys.exit(0 if success else 1)
