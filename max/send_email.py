#!/usr/bin/env python3
"""
Max Email Sender - Kirim email untuk notifikasi artikel
Usage: python3 send_email.py <recipient> <subject> <body>
       python3 send_email.py --article <path> [--recipient <email>]
"""

import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

# Konfigurasi
SMTP_HOST = "mail.taraka.id"
SMTP_PORT = 465  # SSL
SMTP_USER = "blog@taraka.id"
SMTP_PASS = "Blog.215"

def send_email(recipient, subject, body):
    """Kirim email melalui SMTP SSL"""
    msg = EmailMessage()
    msg['From'] = SMTP_USER
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)
    
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
    
    # Remove title from body (judul sudah di subjek)
    body_lines = []
    skipped_title = False
    for line in lines:
        if not skipped_title and line.startswith('# '):
            skipped_title = True
            continue
        body_lines.append(line)
    
    body = '\n'.join(body_lines).strip()
    
    return send_email(recipient, title, body)

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
