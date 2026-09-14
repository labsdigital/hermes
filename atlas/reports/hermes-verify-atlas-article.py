#!/usr/bin/env python3
"""Ad-hoc verification for Atlas article files."""
import os
import sys

reports_dir = "/opt/data/hermes/atlas/reports"
files = [
    "etika-mesin-ai-2026-09-03.md",
    "etika-mesin-ai-2026-09-03.html",
    "etika-mesin-ai-2026-09-03-artistik.png",
    "etika-mesin-ai-diagram.svg",
]

all_ok = True
for f in files:
    path = os.path.join(reports_dir, f)
    if not os.path.exists(path):
        print(f"❌ MISSING: {f}")
        all_ok = False
        continue
    size = os.path.getsize(path)
    if size == 0:
        print(f"⚠️  EMPTY: {f}")
        all_ok = False
    else:
        print(f"✅ {f} ({size:,} bytes)")

# SVG basic check
svg_path = os.path.join(reports_dir, "etika-mesin-ai-diagram.svg")
if os.path.exists(svg_path):
    with open(svg_path, 'r') as fh:
        content = fh.read()
    checks = [
        ('xmlns', 'xmlns=' in content),
        ('viewBox', 'viewBox=' in content),
        ('title', '<title' in content),
        ('root tag', content.strip().startswith('<?xml') or content.strip().startswith('<svg')),
    ]
    for name, ok in checks:
        print(f"{'✅' if ok else '❌'} SVG: {name}")
        if not ok:
            all_ok = False

# PNG check (accept JPEG since polli sometimes returns jpg despite extension)
png_path = os.path.join(reports_dir, "etika-mesin-ai-2026-09-03-artistik.png")
if os.path.exists(png_path):
    with open(png_path, 'rb') as fh:
        header = fh.read(8)
    is_png = header[:4] == b'\x89PNG'
    is_jpeg = header[:2] == b'\xff\xd8'
    img_type = "PNG" if is_png else ("JPEG" if is_jpeg else "UNKNOWN")
    is_valid_image = is_png or is_jpeg
    print(f"{'✅' if is_valid_image else '❌'} Image: {img_type} format ({'valid' if is_valid_image else 'invalid'})")
    if not is_valid_image:
        all_ok = False

# MD word count
md_path = os.path.join(reports_dir, "etika-mesin-ai-2026-09-03.md")
if os.path.exists(md_path):
    with open(md_path, 'r') as fh:
        text = fh.read()
    words = len(text.split())
    print(f"{'✅' if words >= 800 else '⚠️'} MD word count: {words} (min 800)")
    if words < 800:
        all_ok = False

# Check image URLs in MD
if os.path.exists(md_path):
    with open(md_path, 'r') as fh:
        md_content = fh.read()
    has_artistik = 'etika-mesin-ai-2026-09-03-artistik.png' in md_content
    has_diagram = 'etika-mesin-ai-diagram.svg' in md_content
    print(f"{'✅' if has_artistik else '❌'} MD references artistik PNG")
    print(f"{'✅' if has_diagram else '❌'} MD references diagram SVG")
    if not has_artistik or not has_diagram:
        all_ok = False

print("\n" + ("✅ All checks passed" if all_ok else "❌ Some checks failed"))
sys.exit(0 if all_ok else 1)
