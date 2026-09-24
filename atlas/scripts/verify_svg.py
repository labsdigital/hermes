#!/usr/bin/env python3
"""Verify SVG diagram for Atlas article: pekerjaan-mesin-ai-2026-09-03"""
import xml.etree.ElementTree as ET
from pathlib import Path

svg_path = Path("/opt/data/hermes/atlas/reports/pekerjaan-mesin-ai-2026-09-03.svg")

# 1. File exists and is readable
assert svg_path.exists(), "SVG file not found"
print("✅ File exists")

# 2. Valid XML / SVG
try:
    tree = ET.parse(svg_path)
    root = tree.getroot()
except ET.ParseError as e:
    raise AssertionError(f"Invalid XML: {e}")
print(f"✅ Valid XML — root tag: {root.tag}")

# 3. Required attributes present
assert root.get("xmlns"), "Missing xmlns attribute"
assert root.get("viewBox"), "Missing viewBox attribute"
print(f"✅ Has xmlns and viewBox ({root.get('viewBox')})")

# 4. Key elements exist
ns = {"svg": "http://www.w3.org/2000/svg"}
defs = root.find("svg:defs", ns)
rects = root.findall(".//svg:rect", ns)
texts = root.findall(".//svg:text", ns)
paths = root.findall(".//svg:path", ns)

print(f"✅ <defs>: {'present' if defs is not None else 'missing'}")
print(f"✅ <rect> elements: {len(rects)}")
print(f"✅ <text> elements: {len(texts)}")
print(f"✅ <path> elements: {len(paths)}")

# 5. No XML declaration (per SVG fix memory)
content = svg_path.read_text(encoding="utf-8")
assert not content.lstrip().startswith("<?xml"), "Contains XML declaration — should be stripped"
print("✅ No XML declaration (correct for inline embedding)")

print("\n🎉 SVG verified successfully!")
