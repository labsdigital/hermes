#!/usr/bin/env python3
"""
HTML Validation Tool for Atlas Articles
Validates HTML output from md_to_html conversion
Converts remaining markdown syntax to proper HTML
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
        'valid': True,
        'fixes_applied': []
    }
    
    try:
        html_content = Path(html_path).read_text(encoding='utf-8')
    except Exception as e:
        results['errors'].append(f"Cannot read file: {e}")
        results['valid'] = False
        return results
    
    original_content = html_content
    
    # Check for markdown image syntax still present (![alt](url))
    markdown_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', html_content)
    if markdown_images:
        results['errors'].append(f"Markdown image syntax found: {len(markdown_images)} instances")
        results['valid'] = False
        for alt, url in markdown_images:
            results['warnings'].append(f"  - ![{alt}]({url})")
    
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
    
    # Check for markdown syntax still present
    markdown_patterns = [
        (r'\*\*(.+?)\*\*', r'<strong>\1</strong>', 'bold'),
        (r'\*(.+?)\*', r'<em>\1</em>', 'italic'),
        (r'`(.+?)`', r'<code>\1</code>', 'inline code'),
        (r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', 'links'),
    ]
    
    for pattern, replacement, name in markdown_patterns:
        matches = re.findall(pattern, html_content)
        if matches:
            results['warnings'].append(f"Unc converted {name}: {len(matches)} instances")
    
    # Check for raw URLs (not linked)
    raw_urls = re.findall(r'https?://[^\s<>"\')]+', html_content)
    if raw_urls and len(raw_urls) > 5:  # Allow some URLs
        results['warnings'].append(f"Potential raw URLs found: {len(raw_urls)} instances")
    
    return results


def fix_html(html_path: str) -> bool:
    """Apply automatic fixes to HTML file."""
    content = Path(html_path).read_text(encoding='utf-8')
    original = content
    fixes = []
    
    # Fix 1: Convert markdown images to HTML img tags
    markdown_images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    if markdown_images:
        for alt, url in markdown_images:
            # Clean up URL
            url = url.replace('https://https://', 'https://')
            # Convert to HTML img tag
            html_img = f'<div class="article-image"><img src="{url}" alt="{alt}" /></div>'
            content = content.replace(f'![{alt}]({url})', html_img)
        fixes.append(f"Converted {len(markdown_images)} markdown images to HTML img tags")
    
    # Fix 2: Fix double HTTPS
    if 'https://https://' in content:
        content = content.replace('https://https://', 'https://')
        fixes.append("Fixed double HTTPS URLs")
    
    # Fix 3: Fix double slashes in URLs
    fixed = re.sub(r'https://labsdigital\.github\.io/hermes/atlas/reports/reports/',
                   'https://labsdigital.github.io/hermes/atlas/reports/', content)
    if fixed != content:
        content = fixed
        fixes.append("Fixed double path segments in URLs")
    
    # Fix 4: Convert uncached markdown bold (if any slipped through)
    # This handles cases where **bold** appears outside of proper HTML
    bold_matches = re.findall(r'\*\*(.+?)\*\*', content)
    if bold_matches:
        for match in bold_matches:
            # Only convert if not already inside HTML tags
            pattern = f'**{match}**'
            if pattern in content and f'<strong>{match}</strong>' not in content:
                content = content.replace(pattern, f'<strong>{match}</strong>')
        if '**' in content:
            fixes.append("Converted remaining bold markdown to <strong> tags")
    
    # Fix 5: Convert uncached markdown italic
    italic_matches = re.findall(r'\*(.+?)\*', content)
    if italic_matches:
        for match in italic_matches:
            pattern = f'*{match}*'
            if pattern in content and f'<em>{match}</em>' not in content:
                content = content.replace(pattern, f'<em>{match}</em>')
        if '*' in content and '<em>' not in content:
            fixes.append("Converted remaining italic markdown to <em> tags")
    
    # Fix 6: Convert uncached inline code
    code_matches = re.findall(r'`(.+?)`', content)
    if code_matches:
        for match in code_matches:
            pattern = f'`{match}`'
            if pattern in content and f'<code>{match}</code>' not in content:
                content = content.replace(pattern, f'<code>{match}</code>')
        if '`' in content and '<code>' not in content:
            fixes.append("Converted remaining inline code markdown to <code> tags")
    
    if content != original:
        Path(html_path).write_text(content, encoding='utf-8')
        return True
    return False


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Validate Atlas article HTML')
    parser.add_argument('html_file', help='Path to HTML file')
    parser.add_argument('--fix', action='store_true', help='Apply automatic fixes')
    parser.add_argument('--verbose', action='store_true', help='Show detailed output')
    args = parser.parse_args()
    
    print(f"Validating: {args.html_file}\n")
    
    if args.fix:
        print("Applying fixes...")
        fixed = fix_html(args.html_file)
        if fixed:
            print("✅ Fixes applied")
        else:
            print("No fixes needed")
        print()
    
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
        print("✅ No issues found - HTML is valid!")
    
    return 0 if results['valid'] else 1


if __name__ == '__main__':
    sys.exit(main())
