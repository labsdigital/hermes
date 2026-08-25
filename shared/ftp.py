#!/usr/bin/env python3
"""
FTP Upload Utility - Alias for shared ftp_upload.py
Usage: python3 ftp.py <args...>
"""

import sys
import os

# Add shared directory to path
sys.path.insert(0, '/opt/data/hermes/shared')

from ftp_upload import deploy_agent, upload_single

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 ftp.py --deploy <agent> [type]")
        print("       python3 ftp.py <file> [remote_path]")
        sys.exit(1)
    
    if sys.argv[1] == "--deploy":
        agent = sys.argv[2]
        content_type = sys.argv[3] if len(sys.argv) > 3 else "all"
        deploy_agent(agent, content_type)
    else:
        file_path = sys.argv[1]
        remote_path = sys.argv[2] if len(sys.argv) > 2 else None
        upload_single(file_path, remote_path)
