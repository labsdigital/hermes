#!/usr/bin/env python3
"""Quick SVG validation for ai-emosi-diagram.svg"""
import sys
import xml.etree.ElementTree as ET

svg_path = "/opt/data/hermes/atlas/reports/ai-emosi-diagram.svg"

try:
    tree = ET.parse(svg_path)
    root = tree.getroot()
    
    # Check namespace
    ns = "http://www.w3.org/2000/svg"
    assert root.tag == f"{{{ns}}}svg", f"Wrong tag: {root.tag}"
    
    # Check viewBox
    viewBox = root.get("viewBox")
    assert viewBox, "Missing viewBox"
    assert viewBox == "0 0 600 400", f"Unexpected viewBox: {viewBox}"
    
    # Check required attributes
    xmlns = root.get("xmlns")
    assert xmlns == ns, f"Wrong xmlns: {xmlns}"
    
    # Check role/title for accessibility
    title = root.find(f"{{{ns}}}title")
    assert title is not None, "Missing <title>"
    assert title.text and len(title.text) > 5, "Title too short"
    
    # Count key elements
    circles = root.findall(f"{{{ns}}}circle")
    paths = root.findall(f"{{{ns}}}path")
    rects = root.findall(f"{{{ns}}}rect")
    texts = root.findall(f"{{{ns}}}text")
    
    print(f"✅ SVG valid")
    print(f"   viewBox: {viewBox}")
    print(f"   Elements: {len(circles)} circles, {len(paths)} paths, {len(rects)} rects, {len(texts)} texts")
    print(f"   Title: '{title.text}'")
    print(f"✅ All checks passed")
    sys.exit(0)
    
except Exception as e:
    print(f"❌ Validation failed: {e}")
    sys.exit(1)
