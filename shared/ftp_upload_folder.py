#!/usr/bin/env python3
"""
Upload folder to FTP (recursive)
Usage: python3 ftp_upload_folder.py <folder> <remote_path>
"""

import ftplib
import sys
from pathlib import Path

# CONFIGURATION
FTP_HOST = "ftp.rumahguru.org"
FTP_USER = "hermesftp@taraka.id"
FTP_PASS = "H32m35."
FTP_PORT = 21

def upload_folder(local_folder, remote_path):
    """Upload entire folder recursively"""
    try:
        ftp = ftplib.FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=30)
        ftp.login(FTP_USER, FTP_PASS)
        ftp.encoding = "utf-8"
        
        local = Path(local_folder)
        urls = []
        
        # Ensure remote directory exists
        try:
            ftp.cwd(remote_path)
        except:
            parts = remote_path.strip('/').split('/')
            current = ""
            for part in parts:
                current = f"{current}/{part}"
                try:
                    ftp.cwd(current)
                except:
                    ftp.mkd(part)
                    ftp.cwd(current)
        
        print(f"📤 Uploading {local_folder}/ to {remote_path}...")
        
        # Upload all files
        for file in sorted(local.rglob("*")):
            if file.is_file():
                rel_path = file.relative_to(local)
                remote_file_path = f"{remote_path}{rel_path}"
                remote_dir = str(Path(remote_file_path).parent)
                
                # Create remote directory
                try:
                    ftp.cwd(remote_dir)
                except:
                    parts = remote_dir.strip('/').split('/')
                    current = ""
                    for part in parts:
                        current = f"{current}/{part}"
                        try:
                            ftp.cwd(current)
                        except:
                            ftp.mkd(part)
                            ftp.cwd(current)
                
                # Upload file
                filename = file.name
                print(f"   📄 {rel_path}")
                with open(file, 'rb') as fp:
                    ftp.storbinary(f'STOR {filename}', fp)
                
                url = f"https://{FTP_HOST}{remote_file_path}"
                urls.append(url)
        
        ftp.quit()
        
        print("")
        print("✅ Upload successful!")
        print("")
        print("📰 Content URLs:")
        for url in urls:
            print(f"   {url}")
        
        return urls
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 ftp_upload_folder.py <folder> <remote_path>")
        print("Example: python3 ftp_upload_folder.py elon/gerak-parabola /elon/gerak-parabola/")
        sys.exit(1)
    
    folder = sys.argv[1]
    remote = sys.argv[2]
    
    if not Path(folder).exists():
        print(f"❌ Folder not found: {folder}")
        sys.exit(1)
    
    upload_folder(folder, remote)
