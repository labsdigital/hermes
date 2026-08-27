#!/usr/bin/env python3
"""
Chalbi Email Sender - Kirim email untuk notifikasi artikel
Usage: python3 send_email.py <recipient> <subject> <body>
       python3 send_email.py --article <path> [--recipient <email>]
"""

import smtplib
import sys
import re
from email.message import EmailMessage
from pathlib import Path

# Konfigurasi
SMTP_HOST = "mail.taraka.id"
SMTP_PORT = 465  # SSL
SMTP_USER = "blog@taraka.id"
SMTP_PASS = "Blog.215"

def md_to_html(md_text):
    """Convert markdown to HTML dengan CSS dasar saja"""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    in_quote = False
    in_svg_block = False
    svg_content = ""
    svg_counter = 0
    
    for line in lines:
        # Handle SVG blocks (```svg ... ```)
        if line.strip() == '```svg':
            in_svg_block = True
            svg_content = '<div class="svg-diagram">\n'
            continue
        
        if in_svg_block:
            if line.strip() == '```':
                # End of SVG block - remove XML declaration for email compatibility
                in_svg_block = False
                # Extract just the SVG content (without div wrapper)
                svg_raw = svg_content.replace('<div class="svg-diagram">\n', '').replace('\n</div>', '').strip()
                # Remove XML declaration if present
                if svg_raw.startswith('<?xml'):
                    svg_raw = re.sub(r'^<\?xml[^?]*\?>\s*', '', svg_raw)
                svg_content = f'<div class="svg-diagram">\n{svg_raw}\n</div>'
                html_lines.append(svg_content)
                svg_counter += 1
                continue
            svg_content += line + '\n'
            continue
        
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                html_lines.append('</code></pre>')
                in_code_block = False
            else:
                html_lines.append('<pre><code>')
                in_code_block = True
            continue
        
        if in_code_block:
            html_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            continue
        
        # Headers
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        # Horizontal rule
        elif line == '---':
            html_lines.append('<hr>')
        # Quote blocks (Rumi quotes)
        elif line.startswith('> ') or line.startswith('❝'):
            if not in_quote:
                html_lines.append('<blockquote>')
                in_quote = True
            content = line.lstrip('> ❝').strip()
            html_lines.append(f'<p>{content}</p>')
        elif in_quote and line.strip() == '':
            html_lines.append('</blockquote>')
            in_quote = False
        # Bold
        elif '**' in line:
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
            html_lines.append(f'<p>{line}</p>')
        # Lists
        elif line.startswith('- '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue
        # Tables
        elif line.startswith('|'):
            # Simple table handling
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(c.startswith('**') or c.endswith('**') for c in cells):
                # Header row
                html_lines.append('<thead><tr>')
                for cell in cells:
                    cell = cell.replace('**', '').replace('|', '')
                    html_lines.append(f'<th>{cell}</th>')
                html_lines.append('</tr></thead><tbody>')
            else:
                # Data row
                html_lines.append('<tr>')
                for cell in cells:
                    cell = cell.replace('**', '').replace('|', '')
                    html_lines.append(f'<td>{cell}</td>')
                html_lines.append('</tr>')
        # Markdown images: ![alt](url) → <img>
        elif '![[' in line or re.match(r'!\[.*\]\(.*\)', line):
            img_match = re.search(r'!\[(.*?)\]\((.*?)\)', line)
            if img_match:
                alt = img_match.group(1)
                url = img_match.group(2).strip()
                html_lines.append(f'<div style="text-align:center;margin:20px 0;"><img src="{url}" alt="{alt}" style="max-width:100%;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.1);" /></div>')
            else:
                html_lines.append(f'<p>{line}</p>')
        # Regular paragraph
        else:
            html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    if in_quote:
        html_lines.append('</blockquote>')
    
    return '\n'.join(html_lines)

def send_email(recipient, subject, body_html):
    """Kirim email melalui SMTP SSL dengan HTML body"""
    msg = EmailMessage()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.add_alternative(f"""\
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<style>
    .svg-diagram {{ max-width: 100%; margin: 30px 0; }}
    .svg-diagram svg {{ width: 100%; height: auto; }}
    blockquote {{ border-left: 4px solid #8b4513; padding-left: 20px; margin: 20px 0; font-style: italic; color: #555; }}
    pre {{ background: #f5f5f5; padding: 15px; overflow-x: auto; border-radius: 8px; }}
    h1 {{ color: #8b4513; border-bottom: 2px solid #d4a574; padding-bottom: 10px; }}
    h2 {{ color: #a0522d; margin-top: 30px; }}
    h3 {{ color: #cd853f; }}
</style>
<body>
{body_html}
</body>
</html>
""", subtype='html')
    
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASS)
            server.send_message(msg)
        return True, f"Email berhasil dikirim ke {recipient}"
    except Exception as e:
        return False, f"Error: {e}"

def send_article_notification(article_path, recipient="tamimnasa.chalbi@blogger.com"):
    """Kirim notifikasi artikel baru ke multiple recipients"""
    article = Path(article_path)
    if not article.exists():
        return False, "File tidak ditemukan"
    
    content = article.read_text()
    lines = content.split('\n')
    
    # Extract title (first line starting with #)
    title = ""
    for line in lines:
        if line.startswith('# '):
            title = line[2:].strip()
            break
    
    # Use full title as subject
    subject = title
    
    # Remove title and author line from content
    body_lines = []
    skipped_title = False
    skipped_author = False
    for line in lines:
        if not skipped_title and line.startswith('# '):
            skipped_title = True
            continue
        if not skipped_author and line.startswith('*Oleh'):
            skipped_author = True
            continue
        body_lines.append(line)
    
    body_md = '\n'.join(body_lines).strip()
    body_html = md_to_html(body_md)
    
    # Default recipients (primary + secondary)
    default_recipients = [
        "tamimnasa.chalbi@blogger.com",
        "tamimnasa@gmail.com"
    ]
    
    # If custom recipient specified, use that instead
    if recipient not in default_recipients:
        recipients = [recipient]
    else:
        recipients = default_recipients
    
    # Send to all recipients
    results = []
    for r in recipients:
        success, msg = send_email(r, subject, body_html)
        results.append(msg)
    
    return all(r[0] for r in results), "; ".join(results)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 send_email.py <recipient> <subject> <body>")
        print("Or: python3 send_email.py --article <path> [--recipient <email>]")
        sys.exit(1)

    if sys.argv[1] == "--article":
        article_path = sys.argv[2]
        recipient = "tamimnasa.chalbi@blogger.com"
        if len(sys.argv) > 3 and sys.argv[3] == "--recipient":
            recipient = sys.argv[4]
        success, msg = send_article_notification(article_path, recipient)
        print(msg)
        sys.exit(0 if success else 1)
    else:
        recipient = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]
        success, msg = send_email(recipient, subject, body)
        print(msg)
        sys.exit(0 if success else 1)
