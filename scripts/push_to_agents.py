#!/usr/bin/env python3
"""
Push Atlas articles to labsdigital/agents repo
Usage: python3 push_to_agents.py <filename>
"""
import subprocess
import sys
import os

HERMES_REPO = "/opt/data/hermes"
AGENTS_CLONE = "/tmp/agents-clone"
AGENTS_REMOTE = "https://github.com/labsdigital/agents.git"

def push_to_agents(filename):
    """Push file to agents repo"""
    
    # Ensure agents clone exists
    if not os.path.exists(AGENTS_CLONE):
        subprocess.run(["git", "clone", AGENTS_REMOTE, AGENTS_CLONE], check=True)
    
    # Get base filename without extension
    base = os.path.splitext(filename)[0]
    
    # Copy all related files
    files_to_copy = [
        f"{base}.md",
        f"{base}.html",
        f"{base}-diagram.svg",
        f"{base}-artistik.png"
    ]
    
    for f in files_to_copy:
        src = os.path.join(HERMES_REPO, "atlas", "reports", f)
        dst = os.path.join(AGENTS_CLONE, "atlas", "reports", f)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            subprocess.run(["cp", src, dst], check=True)
            print(f"  📋 Copied: {f}")
    
    # Commit and push
    subprocess.run(["git", "-C", AGENTS_CLONE, "add", "."], check=True)
    subprocess.run(["git", "-C", AGENTS_CLONE, "commit", "-m", f"Atlas: {base}"], check=True)
    subprocess.run(["git", "-C", AGENTS_CLONE, "push"], check=True)
    
    print(f"\n✅ Pushed to: https://github.com/labsdigital/agents/tree/main/atlas/reports")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 push_to_agents.py <filename>")
        sys.exit(1)
    
    push_to_agents(sys.argv[1])
