#!/usr/bin/env python3
"""
Atlas Article Publisher - Dual Format (.md + .html)
Publishes articles to GitHub in both Markdown and HTML formats.
No external dependencies required.
"""

import argparse
import re
import sys
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
                in_code_block = True
                continue
            elif in_svg_block:
                # End of SVG block - close div and add inline SVG
                in_svg_block = False
                svg_content += '\n</div>'
                html_lines.append(svg_content)
                continue
            elif in_code_block:
                in_code_block = False
                continue
        
        # Handle SVG blocks
        if line.strip() == '```svg':
            in_svg_block = True
            svg_content = '<div class="svg-diagram">\n'
            continue
        
        if in_svg_block:
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
        
        # Extract title
        if line.startswith('# ') and not title:
            title = line[2:].strip()
            html_lines.append(f'<h1>{line[2:]}</h1>')
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
    """Create complete HTML document."""
    return f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Atlas Essays</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            line-height: 1.8;
            color: #1a1a1a;
            background: #fafafa;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 40px 20px;
        }}
        header {{
            text-align: center;
            padding: 60px 20px;
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 40px;
        }}
        h1 {{
            font-size: 2.5em;
            color: #1a1a1a;
            margin-bottom: 15px;
            line-height: 1.3;
        }}
        h2 {{
            font-size: 1.8em;
            margin: 40px 0 20px;
            color: #2a2a2a;
        }}
        h3 {{
            font-size: 1.4em;
            margin: 30px 0 15px;
            color: #333;
        }}
        .meta {{
            font-size: 0.9em;
            color: #666;
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
            border-left: 4px solid #e74c3c;
            padding-left: 20px;
            margin: 30px 0;
            font-style: italic;
            color: #555;
        }}
        article pre {{
            background: #f4f4f4;
            padding: 20px;
            overflow-x: auto;
            border-radius: 8px;
            margin: 20px 0;
        }}
        article code {{
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        article img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            margin: 20px 0;
        }}
        .svg-diagram {{
            max-width: 100%;
            margin: 30px 0;
        }}
        .svg-diagram svg {{
            width: 100%;
            height: auto;
        }}
        hr {{
            border: none;
            border-top: 1px solid #e0e0e0;
            margin: 40px 0;
        }}
        .footer {{
            margin-top: 60px;
            padding-top: 30px;
            border-top: 1px solid #e0e0e0;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
        .quote-box {{
            background: #fff7ed;
            border: 1px solid #fde68a;
            padding: 20px 30px;
            margin: 30px 0;
            border-radius: 8px;
            font-style: italic;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <p class="meta">Esai Non-Fiksi | {date} | By Atlas</p>
        </header>
        
        <article>
{html_body}
        </article>
        
        <div class="footer">
            <p>Artikel ini diterbitkan oleh <strong>Atlas</strong> - Essay & Nonfiction Writer</p>
            <p>&copy; 2026 Labsdigital. Semua hak dilindungi.</p>
        </div>
    </div>
</body>
</html>'''


def publish_article(article_name: str, base_path: str = '/opt/data/hermes', skip_git: bool = False):
    """Publish article in both .md and .html formats."""
    base = Path(base_path)
    reports = base / 'atlas' / 'reports'
    
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
    
    # Git operations
    if not skip_git:
        print("\n📤 Commit ke GitHub...")
        import subprocess
        
        # Add files
        subprocess.run(['git', 'add', str(md_file), str(html_file)], cwd=base)
        
        # Commit
        commit_msg = f"Atlas: {title}"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd=base)
        
        # Push
        subprocess.run(['git', 'push', 'origin', 'main'], cwd=base)
        print("✅ Dipush ke GitHub")
    
    # Show URLs
    print("\n" + "="*50)
    print("📄 Versi Markdown:")
    print(f"   https://github.com/labsdigital/hermes/blob/main/atlas/reports/{article_name}.md")
    print(f"\n🌐 Versi HTML:")
    print(f"   https://labsdigital.github.io/hermes/atlas/reports/{article_name}.html")
    print("="*50)


def main():
    parser = argparse.ArgumentParser(description='Publish Atlas article in .md and .html formats')
    parser.add_argument('article', help='Article name (without extension)')
    parser.add_argument('--skip-git', action='store_true', help='Skip git operations')
    parser.add_argument('--base', default='/opt/data/hermes', help='Base path')
    
    args = parser.parse_args()
    publish_article(args.article, args.base, args.skip_git)


if __name__ == '__main__':
    main()
