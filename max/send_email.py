#!/usr/bin/env python3
"""
Max Email Sender - Kirim email untuk notifikasi artikel
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
    """Convert markdown to HTML"""
    lines = md_text.split('\n')
    html_lines = []
    in_code_block = False
    in_list = False
    
    for line in lines:
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
        if line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        # Horizontal rule
        elif line == '---':
            html_lines.append('<hr>')
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
        # Regular paragraph
        else:
            html_lines.append(f'<p>{line}</p>')
    
    if in_list:
        html_lines.append('</ul>')
    
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
<body style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.6;">
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

def send_article_notification(article_path, recipient="tamimnasa@gmail.com"):
    """Kirim notifikasi artikel baru"""
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
    
    # Remove title from content
    body_lines = []
    skipped_title = False
    for line in lines:
        if not skipped_title and line.startswith('# '):
            skipped_title = True
            continue
        body_lines.append(line)
    
    body_md = '\n'.join(body_lines).strip()
    body_html = md_to_html(body_md)
    
    return send_email(recipient, title, body_html)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 send_email.py <recipient> <subject> <body>")
        print("Or: python3 send_email.py --article <path> [--recipient <email>]")
        sys.exit(1)
    
    if sys.argv[1] == "--article":
        article_path = sys.argv[2]
        recipient = "tamimnasa@gmail.com"
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
