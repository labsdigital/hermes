#!/usr/bin/env python3
"""
Chalbi Article Publisher - Convert MD to HTML with SVG embedding
Usage: python3 publish_article.py <article-name>
"""

import sys
import re
from pathlib import Path
from datetime import datetime


def md_to_html(md_text: str) -> tuple[str, str]:
    """Convert markdown text to HTML string. Returns (title, html_body)."""
    lines = md_text.split('\n')
    title = ""
    html_lines = []
    in_code_block = False
    in_svg_block = False
    svg_content = ""
    
    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            if not in_code_block and not in_svg_block:
                # Check if it's an SVG block
                if line.strip() == '```svg':
                    in_svg_block = True
                    svg_content = '<div class="svg-diagram">\n'
                else:
                    in_code_block = True
                continue
            elif in_svg_block:
                # End of SVG block
                in_svg_block = False
                svg_content += '\n</div>'
                html_lines.append(svg_content)
                continue
            elif in_code_block:
                in_code_block = False
                continue
        
        # Handle SVG content
        if in_svg_block:
            # Remove XML declaration for better compatibility
            if line.strip().startswith('<?xml'):
                continue
            svg_content += line + '\n'
            continue
        
        if in_code_block:
            # Escape HTML in code blocks
            escaped = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_lines.append(f'<pre><code>{escaped}</code></pre>')
            continue
        
        # Skip frontmatter
        if line.startswith('---'):
            continue
        
        # Extract title (skip if already found)
        if line.startswith('# ') and not title:
            title = line[2:].strip()
            continue  # Don't add title here, it will be in header
        
        # Skip author line
        if line.startswith('*Oleh'):
            continue
        
        # Headings
        if line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
            continue
        if line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            html_lines.append('<hr>')
            continue
        
        # Bold
        bold_lines = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
        bold_lines = re.sub(r'\*(.+?)\*', r'<em>\1</em>', bold_lines)
        
        # Links
        bold_lines = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', bold_lines)
        
        # Inline code
        bold_lines = re.sub(r'`(.+?)`', r'<code>\1</code>', bold_lines)
        
        # Empty lines become paragraph breaks
        if line.strip() == '':
            html_lines.append('<br>')
            continue
        
        html_lines.append(f'<p>{bold_lines}</p>')
    
    return title, '\n'.join(html_lines)


def create_html_article(title: str, html_body: str, date: str) -> str:
    """Create complete HTML document with Chalbi styling."""
    return f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Chalbi - Rumi Essays</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.8;
            color: #2c1810;
            background: linear-gradient(135deg, #faf6f0 0%, #f5ebe0 100%);
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        header {{
            text-align: center;
            padding: 60px 20px;
            border-bottom: 2px solid #d4a574;
            margin-bottom: 40px;
            background: linear-gradient(to bottom, #fff8f0, #faf6f0);
        }}
        h1 {{
            font-size: 2.2em;
            color: #8b4513;
            margin-bottom: 15px;
            line-height: 1.3;
        }}
        h2 {{
            font-size: 1.6em;
            margin: 40px 0 20px;
            color: #a0522d;
            border-left: 4px solid #d4a574;
            padding-left: 15px;
        }}
        h3 {{
            font-size: 1.3em;
            margin: 30px 0 15px;
            color: #cd853f;
        }}
        .meta {{
            font-size: 0.95em;
            color: #8b7355;
            font-style: italic;
        }}
        article {{
            font-size: 1.1em;
        }}
        article p {{
            margin-bottom: 20px;
            text-align: justify;
        }}
        article blockquote {{
            border-left: 4px solid #8b4513;
            padding-left: 20px;
            margin: 30px 0;
            font-style: italic;
            color: #5d4a35;
            background: #fff8f0;
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
        }}
        article pre {{
            background: #f5ebe0;
            padding: 20px;
            overflow-x: auto;
            border-radius: 8px;
            margin: 20px 0;
        }}
        article code {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #8b4513;
        }}
        article img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 4px 12px rgba(139, 69, 19, 0.15);
        }}
        .svg-diagram {{
            max-width: 100%;
            margin: 30px 0;
            background: #fff8f0;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(139, 69, 19, 0.1);
        }}
        .svg-diagram svg {{
            width: 100%;
            height: auto;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e0c8b0;
            margin: 40px 0;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 2px solid #d4a574;
            text-align: center;
            color: #8b7355;
            font-size: 0.9em;
        }}
        .quote-box {{
            background: linear-gradient(135deg, #fff8f0, #faf6f0);
            border: 1px solid #e6d5b8;
            padding: 25px 30px;
            margin: 30px 0;
            border-radius: 12px;
            font-style: italic;
            text-align: center;
        }}
        .persian-quote {{
            font-size: 1.2em;
            color: #8b4513;
            text-align: center;
            margin: 20px 0;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="meta">Oleh Chalbi | {date}</p>
        </header>
        
        <article>
{html_body}
        </article>
        
        <div class="footer">
            <p>Artikel ini diterbitkan oleh <strong>Chalbi</strong> - Rumi & Masnavi Scholar</p>
            <p>&copy; 2026 Labsdigital. Semua hak dilindungi.</p>
        </div>
    </div>
</body>
</html>'''


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 publish_article.py <article-name>")
        print("Example: python3 publish_article.py kesadaran-2026-08-27")
        sys.exit(1)
    
    article_name = sys.argv[1]
    base = Path('/opt/data/hermes')
    reports = base / 'chalbi' / 'reports'
    
    md_file = reports / f"{article_name}.md"
    html_file = reports / f"{article_name}.html"
    
    if not md_file.exists():
        print(f"❌ File tidak ditemukan: {md_file}")
        sys.exit(1)
    
    # Read markdown
    md_content = md_file.read_text(encoding='utf-8')
    date = datetime.now().strftime("%B %d, %Y")
    
    # Convert to HTML
    print(f"📝 Mengonversi {md_file.name} → {html_file.name}...")
    title, html_body = md_to_html(md_content)
    html_doc = create_html_article(title, html_body, date)
    html_file.write_text(html_doc, encoding='utf-8')
    print(f"✅ HTML dibuat: {title}")
    print(f"📊 Ukuran: {html_file.stat().st_size / 1024:.1f} KB")
    
    # Count SVG diagrams
    svg_count = md_content.count('```svg')
    print(f"🎨 SVG diagrams embedded: {svg_count}")


if __name__ == '__main__':
    main()
