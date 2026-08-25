#!/usr/bin/env python3
"""
Shared FTP Upload Utility - Available for all agents
Usage: python3 ftp_upload.py <file_or_folder> [remote_path]
       python3 ftp_upload.py --deploy <type>
"""

import ftplib
import sys
import os
from pathlib import Path

# CONFIGURATION - Shared across all agents
FTP_HOST = "ftp.rumahguru.org"
FTP_USER = "hermesftp@taraka.id"
FTP_PASS = "H32m35."
FTP_PORT = 21

# Default remote paths by agent
DEFAULT_PATHS = {
    "chalbi": "/chalbi/",
    "max": "/max/",
    "elon": "/elon/",
    "atlas": "/atlas/",
    "taraka": "/taraka/",
}

def connect_ftp():
    """Connect to FTP server"""
    ftp = ftplib.FTP()
    ftp.connect(FTP_HOST, FTP_PORT, timeout=30)
    ftp.login(FTP_USER, FTP_PASS)
    ftp.encoding = "utf-8"
    return ftp

def upload_file(ftp, local_path, remote_path):
    """Upload a single file"""
    filename = Path(local_path).name
    print(f"   📤 {filename}")
    with open(local_path, 'rb') as fp:
        ftp.storbinary(f'STOR {remote_path}{filename}', fp)
    return f"https://{FTP_HOST}{remote_path}{filename}"

def upload_folder(ftp, local_folder, remote_path):
    """Upload entire folder"""
    local = Path(local_folder)
    urls = []
    
    for file in local.rglob("*"):
        if file.is_file():
            # Calculate relative path
            rel_path = file.relative_to(local)
            remote_file_path = f"{remote_path}{rel_path}"
            remote_dir = str(Path(remote_file_path).parent)
            
            # Create remote directory
            try:
                ftp.cwd(remote_dir)
            except:
                # Create nested directories
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
            urls.append(upload_file(ftp, file, f"{remote_dir}/"))
    
    return urls

def deploy_agent(agent_name, content_type="all"):
    """Deploy all content for an agent"""
    if agent_name not in DEFAULT_PATHS:
        print(f"❌ Unknown agent: {agent_name}")
        print(f"   Available: {', '.join(DEFAULT_PATHS.keys())}")
        return []
    
    remote_path = DEFAULT_PATHS[agent_name]
    ftp = connect_ftp()
    urls = []
    
    try:
        # Ensure directory exists
        try:
            ftp.cwd(remote_path)
        except:
            # Create agent directory
            parts = remote_path.strip('/').split('/')
            current = ""
            for part in parts:
                current = f"{current}/{part}"
                try:
                    ftp.cwd(current)
                except:
                    ftp.mkd(part)
                    ftp.cwd(current)
        
        print(f"🚀 Deploying {agent_name} content...")
        print(f"   Host: {FTP_HOST}")
        print(f"   Path: {remote_path}")
        print("")
        
        if content_type in ["all", "articles"]:
            # Upload articles
            article_dir = Path(f"/opt/data/hermes/{agent_name}/reports")
            if article_dir.exists():
                print(f"📄 Uploading articles from {article_dir}...")
                for f in article_dir.glob("*.md"):
                    url = upload_file(ftp, f, remote_path)
                    urls.append(url)
                print(f"   ✅ Articles uploaded")
                print("")
        
        if content_type in ["all", "apps"]:
            # Upload apps
            app_dir = Path(f"/opt/data/hermes/{agent_name}")
            if app_dir.exists():
                print(f"📱 Uploading apps from {app_dir}...")
                # Find index.html files
                for html in app_dir.rglob("index.html"):
                    if html.parent.name != '__pycache__':
                        rel_path = html.relative_to(app_dir)
                        remote_folder = f"{remote_path}{rel_path.parent}/"
                        try:
                            ftp.cwd(remote_folder)
                        except:
                            parts = remote_folder.strip('/').split('/')
                            current = ""
                            for part in parts:
                                current = f"{current}/{part}"
                                try:
                                    ftp.cwd(current)
                                except:
                                    try:
                                        ftp.mkd(part)
                                        ftp.cwd(current)
                                    except:
                                        pass
                        url = upload_file(ftp, html, remote_folder)
                        urls.append(url)
                        # Also upload related files (CSS, JS, assets)
                        for asset in html.parent.glob("*"):
                            if asset.is_file() and asset.suffix in ['.css', '.js', '.json', '.png', '.jpg', '.svg']:
                                upload_file(ftp, asset, remote_folder)
                print(f"   ✅ Apps uploaded")
        
        ftp.quit()
        
        print("")
        print("✅ Deployment successful!")
        print("")
        print("📰 Content URLs:")
        for url in urls:
            print(f"   • {url}")
        
        return urls
        
    except Exception as e:
        print(f"❌ Error: {e}")
        ftp.quit()
        return []

def upload_single(file_path, remote_path=None, agent=None):
    """Upload a single file"""
    if not Path(file_path).exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    if remote_path is None and agent:
        remote_path = DEFAULT_PATHS.get(agent, "/public/")
    elif remote_path is None:
        remote_path = "/public/"
    
    ftp = connect_ftp()
    
    try:
        # Ensure directory exists
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
        
        url = upload_file(ftp, file_path, remote_path)
        ftp.quit()
        
        print(f"✅ Uploaded: {url}")
        return url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        ftp.quit()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 ftp_upload.py --deploy <agent> [type]")
        print("  python3 ftp_upload.py <file> [remote_path]")
        print("  python3 ftp_upload.py --agent <agent> --file <file>")
        print("")
        print("Examples:")
        print("  python3 ftp_upload.py --deploy chalbi all")
        print("  python3 ftp_upload.py --deploy elon apps")
        print("  python3 ftp_upload.py article.md /chalbi/")
        sys.exit(1)
    
    if sys.argv[1] == "--deploy":
        agent = sys.argv[2]
        content_type = sys.argv[3] if len(sys.argv) > 3 else "all"
        deploy_agent(agent, content_type)
    
    elif sys.argv[1] == "--agent":
        agent = sys.argv[2]
        file_path = sys.argv[4] if len(sys.argv) > 4 else None
        if file_path:
            upload_single(file_path, agent=agent)
        else:
            deploy_agent(agent)
    
    else:
        file_path = sys.argv[1]
        remote_path = sys.argv[2] if len(sys.argv) > 2 else None
        upload_single(file_path, remote_path)
