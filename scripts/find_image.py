#!/usr/bin/env python3
"""
Find and download images from Unsplash or Picsum.
Usage:
  python3 find_image.py --keyword "nature" --agent atlas --mode url
  python3 find_image.py --keyword "AI technology" --agent atlas --mode download --size 1200x800
  python3 find_image.py --agent atlas --mode random --size 800x600
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

import urllib.request
import urllib.parse
import urllib.error
import ssl

# SSL context untuk HTTP request
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def make_request(url: str, headers: dict = None) -> bytes:
    """Make HTTP request with error handling."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {url}", file=sys.stderr)
        return b""
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}", file=sys.stderr)
        return b""


def search_unsplash(keyword: str, per_page: int = 10) -> list[dict]:
    """Search Unsplash for photos by keyword."""
    access_key = os.environ.get("UNSPLASH_ACCESS_KEY", "")
    if not access_key:
        return []

    url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(keyword)}&per_page={per_page}"
    headers = {"Authorization": f"Client-ID {access_key}"}

    data = make_request(url, headers)
    if not data:
        return []

    try:
        result = json.loads(data)
        return result.get("results", [])
    except json.JSONDecodeError:
        return []


def get_random_picsum(count: int = 5) -> list[dict]:
    """Get random photos from Picsum."""
    url = f"https://picsum.photos/v2/list?page=1&limit={count}"
    data = make_request(url)
    if not data:
        return []

    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return []


def download_image(url: str, output_path: Path, width: int = 800) -> bool:
    """Download image from URL to local path."""
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AtlasImageBot/1.0; +https://taraka.id)"
    }

    # For Picsum, construct the direct image URL
    if "picsum.photos" in url or "/id/" in url:
        # Extract photo ID and construct proper URL
        if "/id/" in url:
            parts = url.split("/id/")
            photo_id = parts[1].split("/")[0]
            img_url = f"https://picsum.photos/id/{photo_id}/{width}/{int(width * 0.75)}"
        else:
            img_url = url
    elif "unsplash.com" in url:
        # For Unsplash, use their direct image endpoint
        # Extract photo ID from URL
        import re
        match = re.search(r'photo/([a-zA-Z0-9_-]+)', url)
        if match:
            photo_id = match.group(1)
            img_url = f"https://images.unsplash.com/photo-{photo_id}?w={width}&q=80"
        else:
            img_url = url
    else:
        img_url = url

    data = make_request(img_url, headers)
    if not data:
        return False

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(data)
    return True


def get_unsplash_download_url(photo: dict, width: int = 1200) -> str:
    """Get high-quality download URL from Unsplash photo."""
    urls = photo.get("urls", {})
    # Try regular size first, fallback to full
    return urls.get("regular", urls.get("full", ""))


def format_output(results: list[dict], mode: str, agent: str, size: tuple[int, int], keyword: str = "") -> str:
    """Format results for display."""
    lines = []
    base_path = Path(f"/opt/data/hermes/images/{agent}")

    for r in results:
        if "urls" in r:  # Unsplash
            src = "Unsplash"
            url = get_unsplash_download_url(r, size[0])
            author = r.get("user", {}).get("name", "Unknown")
            username = r.get("user", {}).get("username", "unknown")
            photo_id = r.get("id", "")
            local_filename = f"{agent}-{datetime.now().strftime('%Y%m%d')}-{photo_id}.jpg"
        elif "id" in r:  # Picsum
            src = "Picsum"
            photo_id = r.get("id", "")
            # Use direct Picsum URL format for download
            url = f"https://picsum.photos/id/{photo_id}/{size[0]}/{int(size[0] * 0.75)}"
            author = r.get("author", "Unknown")
            username = ""
            local_filename = f"{agent}-{datetime.now().strftime('%Y%m%d')}-{photo_id}.jpg"
        else:
            continue

        if mode == "url":
            # Return direct URL
            if src == "Unsplash" and url:
                lines.append(f"✅ {url}")
            elif src == "Picsum":
                lines.append(f"✅ {url}")
            lines.append(f"   Source: {src} | Author: {author}{' (@' + username + ')' if username else ''}")
        elif mode == "html":
            # Return HTML img tag with GitHub raw URL
            github_url = f"https://raw.githubusercontent.com/labsdigital/hermes/main/images/{agent}/{local_filename}"
            lines.append(f'<img src="{github_url}" alt="{keyword}" width="{size[0]}" height="{int(size[0] * 0.75)}">')
            lines.append(f"   Source: {src} | Author: {author}{' (@' + username + ')' if username else ''}")
            # Also download the file
            output_path = base_path / local_filename
            if download_image(url, output_path, size[0]):
                ftp_url = f"https://taraka.id/hermes/images/{agent}/{local_filename}"
                lines.append(f"   FTP: {ftp_url}")
        else:  # download
            output_path = base_path / local_filename
            if download_image(url, output_path, size[0]):
                web_url = f"https://taraka.id/hermes/images/{agent}/{local_filename}"
                lines.append(f"✅ Downloaded: {web_url}")
                lines.append(f"   Local: {output_path}")
            else:
                lines.append(f"❌ Failed: {local_filename}")
            lines.append(f"   Author: {author} | Source: {src}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Find and download images from Unsplash/Picsum")
    parser.add_argument("--keyword", help="Search keyword (Unsplash only)")
    parser.add_argument("--agent", default="atlas", help="Agent name for storage folder")
    parser.add_argument("--mode", choices=["url", "download", "html", "random"], default="url",
                        help="Output mode: url (live), download (local), or html (img tag)")
    parser.add_argument("--size", default="1200x800", help="WidthxHeight for download")
    parser.add_argument("--count", type=int, default=1, help="Number of images")
    args = parser.parse_args()

    width, height = map(int, args.size.split("x"))
    results = []

    if args.mode == "random":
        # Use Picsum for random images
        picsum_photos = get_random_picsum(args.count)
        for p in picsum_photos:
            results.append(p)
    elif args.keyword:
        # Try Unsplash first
        unsplash_photos = search_unsplash(args.keyword, args.count)
        if unsplash_photos:
            results = unsplash_photos
        else:
            # Fallback to Picsum random
            print("⚠️  No Unsplash API key found, using Picsum random images")
            picsum_photos = get_random_picsum(args.count)
            results = picsum_photos
    else:
        print("❌ Please provide --keyword or use --mode random")
        sys.exit(1)

    if not results:
        print("❌ No images found")
        sys.exit(1)

    output = format_output(results, args.mode, args.agent, (width, height), keyword=args.keyword)
    print(output)

    # Also write results to JSON for programmatic use
    output_dir = Path(f"/opt/data/hermes/images/{args.agent}")
    output_dir.mkdir(parents=True, exist_ok=True)
    results_file = output_dir / f"search-results-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    results_file.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\n📄 Results saved: {results_file}")


if __name__ == "__main__":
    main()
