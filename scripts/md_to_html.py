#!/usr/bin/env python3
"""
Convert MD article to HTML with embedded images
Usage: python3 md_to_html.py <input.md> <output.html> [--agent atlas]
"""
import argparse
import os
import re
import sys

def md_to_html(md_content, agent=None):
    """Convert markdown to HTML with image embedding"""
    
    lines = md_content.split('\n')
    html_lines = []
    in_code_block = False
    
    for line in lines:
        # Skip YAML frontmatter
        if line.strip().startswith('---') and not in_code_block:
            continue
        
        # Code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            html_lines.append(line)
            continue
        
        if in_code_block:
            html_lines.append(line)
            continue
        
        # Skip empty lines
        if not line.strip():
            html_lines.append('')
            continue
        
        # Headers
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('#### '):
            html_lines.append(f'<h4>{line[5:]}</h4>')
        
        # Bold
        elif '**' in line:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html_lines.append(f'<p>{line}</p>')
        
        # Italic
        elif '*' in line:
            line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
            html_lines.append(f'<p>{line}</p>')
        
        # Links
        elif '[' in line and ']' in line and '(' in line:
            link_match = re.match(r'\[(.+?)\]\((.+?)\)', line)
            if link_match:
                text, url = link_match.groups()
                line = line.replace(f'[{text}]({url})', f'<a href="{url}">{text}</a>')
            html_lines.append(f'<p>{line}</p>')
        
        # Images - convert to HTML img tag
        elif '![' in line:
            img_match = re.match(r'!\[(.+?)\]\((.+?)\)', line)
            if img_match:
                alt, url = img_match.groups()
                # Convert raw GitHub URL to GitHub Pages URL
                if 'raw.githubusercontent.com' in url:
                    url = url.replace('raw.githubusercontent.com/labsdigital/hermes/main/', 
                                     'labsdigital.github.io/hermes/')
                html_lines.append(f'<div class="article-image"><img src="{url}" alt="{alt}" /></div>')
            else:
                html_lines.append(f'<p>{line}</p>')
        
        # Horizontal rules
        elif line.strip() == '---':
            html_lines.append('<hr />')
        
        # Bullet lists
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            html_lines.append(f'<li>{line[2:]}</li>')
        
        # Numbered lists
        elif re.match(r'^\d+\.', line):
            html_lines.append(f'<li>{line.split(".", 1)[1].strip()}</li>')
        
        # Paragraphs
        else:
            html_lines.append(f'<p>{line}</p>')
    
    return '\n'.join(html_lines)

def wrap_html(content, title, agent=None):
    """Wrap content in full HTML template"""
    
    return f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Hermes Blog</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #1a1a2e;
            color: #e6e6e6;
            line-height: 1.8;
        }}
        h1 {{
            color: #667eea;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #f093fb;
            margin-top: 40px;
        }}
        h3 {{
            color: #64ffda;
        }}
        p {{
            margin: 20px 0;
        }}
        .article-image {{
            text-align: center;
            margin: 30px 0;
        }}
        .article-image img {{
            max-width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
        }}
        strong {{
            color: #ffd700;
        }}
        em {{
            color: #e94560;
        }}
        a {{
            color: #64ffda;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        hr {{
            border: none;
            border-top: 1px solid #2d3748;
            margin: 40px 0;
        }}
        ul, ol {{
            padding-left: 30px;
        }}
        li {{
            margin: 10px 0;
        }}
        .meta {{
            color: #8892b0;
            font-size: 14px;
            margin-bottom: 30px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="meta">
        <span>📝 Atlas | </span>
        <span>📅 {datetime.now().strftime('%B %d, %Y')}</span>
    </div>
    {content}
    <hr />
    <p style="color: #8892b0; font-size: 12px;">
        Published by Hermes Agent | <a href="https://github.com/labsdigital/hermes">GitHub</a> | 
        <a href="https://labsdigital.github.io/hermes/blog/">Blog</a>
    </p>
</body>
</html>'''

def main():
    parser = argparse.ArgumentParser(description='Convert MD article to HTML')
    parser.add_argument('input', help='Input MD file')
    parser.add_argument('output', help='Output HTML file')
    parser.add_argument('--agent', default='atlas', help='Agent name')
    
    args = parser.parse_args()
    
    # Read MD file
    with open(args.input, 'r') as f:
        content = f.read()
    
    # Extract title from first header
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else 'Article'
    
    # Convert to HTML
    html_content = md_to_html(content, args.agent)
    
    # Wrap in HTML template
    full_html = wrap_html(html_content, title, args.agent)
    
    # Write output
    with open(args.output, 'w') as f:
        f.write(full_html)
    
    print(f'✓ HTML generated: {args.output}')
    print(f'  Title: {title}')

if __name__ == '__main__':
    from datetime import datetime
    main()
