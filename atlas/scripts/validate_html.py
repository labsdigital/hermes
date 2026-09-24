#!/usr/bin/env python3
"""
HTML Validation Tool for Atlas Articles
Validates HTML output from md_to_html conversion
"""

import re
import sys
from pathlib import Path


def validate_html(html_path: str) -> dict:
    """Validate HTML file and return validation results."""
    results = {
        'file': html_path,
        'errors': [],
        'warnings': [],
        'valid': True
    }
    
    try:
        html_content = Path(html_path).read_text(encoding='utf-8')
    except Exception as e:
        results['errors'].append(f"Cannot read file: {e}")
        results['valid'] = False
        return results
    
    # Check for double HTTPS URLs
    if 'https://https://' in html_content:
        results['errors'].append("Double HTTPS URL found: https://https://")
        results['valid'] = False
    
    # Check for broken image tags
    img_tags = re.findall(r'<img[^>]*>', html_content)
    for img in img_tags:
        src_match = re.search(r'src="([^"]+)"', img)
        if src_match:
            src = src_match.group(1)
            if not src.startswith('http'):
                results['warnings'].append(f"Relative image URL: {src}")
            if 'https://https://' in src:
                results['errors'].append(f"Double HTTPS in image: {src}")
    
    # Check for unclosed tags (common issues)
    # Check for stray closing tags
    close_tags = re.findall(r'</(\w+)>', html_content)
    open_tags = re.findall(r'<(\w+)[^>]*>', html_content)
    
    # Simple validation: check for common patterns
    # Paragraph inside paragraph
    if '<p><p>' in html_content or '</p></p>' in html_content:
        results['warnings'].append("Nested paragraphs detected")
    
    # Check for SVG without proper closing
    svg_open = html_content.count('<svg')
    svg_close = html_content.count('</svg>')
    if svg_open != svg_close:
        results['errors'].append(f"SVG tag mismatch: {svg_open} open, {svg_close} close")
        results['valid'] = False
    
    # Check for proper img closing (self-closing)
    img_open = html_content.count('<img')
    img_closed = html_content.count('/>')
    # This is a simplification - in valid XHTML, img should be self-closing
    
    # Check for proper anchor tags
    anchor_open = html_content.count('<a ')
    anchor_close = html_content.count('</a>')
    if abs(anchor_open - anchor_close) > 2:  # Allow some tolerance
        results['warnings'].append(f"Possible unclosed anchor tags: {anchor_open} open, {anchor_close} close")
    
    # Check for proper heading structure
    headings = re.findall(r'<h[1-6][^>]*>.*?</h[1-6]>', html_content, re.DOTALL)
    heading_levels = []
    for h in headings:
        match = re.search(r'<h(\d)', h)
        if match:
            heading_levels.append(int(match.group(1)))
    
    # Check for skipped heading levels (h1 -> h3 without h2)
    for i in range(1, len(heading_levels)):
        if heading_levels[i] > heading_levels[i-1] + 1:
            results['warnings'].append(f"Skipped heading level: h{heading_levels[i-1]} to h{heading_levels[i]}")
    
    # Check for empty paragraphs
    if '<p></p>' in html_content:
        results['warnings'].append("Empty paragraph tags found")
    
    # Check for proper DOCTYPE and structure
    if '<!DOCTYPE html>' not in html_content:
        results['warnings'].append("Missing DOCTYPE declaration")
    
    if '<html' not in html_content:
        results['errors'].append("Missing HTML tag")
        results['valid'] = False
    
    if '<head>' not in html_content or '</head>' not in html_content:
        results['warnings'].append("Missing or improper head section")
    
    if '<body>' not in html_content or '</body>' not in html_content:
        results['warnings'].append("Missing or improper body section")
    
    return results


def fix_html(html_path: str) -> bool:
    """Apply automatic fixes to HTML file."""
    content = Path(html_path).read_text(encoding='utf-8')
    original = content
    
    # Fix double HTTPS
    content = content.replace('https://https://', 'https://')
    
    # Fix double slashes in URLs
    content = re.sub(r'https://labsdigital\.github\.io/hermes/atlas/reports/reports/',
                     'https://labsdigital.github.io/hermes/atlas/reports/', content)
    
    if content != original:
        Path(html_path).write_text(content, encoding='utf-8')
        return True
    return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Validate Atlas article HTML')
    parser.add_argument('html_file', help='Path to HTML file')
    parser.add_argument('--fix', action='store_true', help='Apply automatic fixes')
    args = parser.parse_args()
    
    print(f"Validating: {args.html_file}\n")
    
    if args.fix:
        print("Applying fixes...")
        fixed = fix_html(args.html_file)
        if fixed:
            print("✅ Fixes applied")
        else:
            print("No fixes needed")
    
    results = validate_html(args.html_file)
    
    print(f"File: {results['file']}")
    print(f"Status: {'✅ VALID' if results['valid'] else '❌ INVALID'}\n")
    
    if results['errors']:
        print("❌ Errors:")
        for err in results['errors']:
            print(f"  - {err}")
        print()
    
    if results['warnings']:
        print("⚠️  Warnings:")
        for warn in results['warnings']:
            print(f"  - {warn}")
        print()
    
    if not results['errors'] and not results['warnings']:
        print("✅ No issues found")
    
    return 0 if results['valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
