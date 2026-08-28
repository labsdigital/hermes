#!/usr/bin/env python3
"""
Add article to Hermes Blog
Usage: python3 add_blog_article.py <agent> <title> <date> <excerpt> <words> <url> [tags]
"""
import json
import sys
import os
from datetime import datetime

BLOG_DIR = "/opt/data/hermes/blog"

def add_article(agent, title, date, excerpt, words, url, tags=None):
    """Add article to agent's blog"""
    if tags is None:
        tags = []
    
    articles_file = os.path.join(BLOG_DIR, agent, "articles.json")
    
    # Load existing articles
    if os.path.exists(articles_file):
        with open(articles_file, 'r') as f:
            articles = json.load(f)
    else:
        articles = []
    
    # Get max ID
    max_id = max([a['id'] for a in articles]) if articles else 0
    
    # Create new article
    article = {
        "id": max_id + 1,
        "title": title,
        "date": date,
        "excerpt": excerpt,
        "url": url,
        "words": words,
        "tags": tags
    }
    
    articles.append(article)
    
    # Save
    with open(articles_file, 'w') as f:
        json.dump(articles, f, indent=2)
    
    print(f"✓ Added article to {agent}/articles.json")
    print(f"  ID: {article['id']}")
    print(f"  Title: {title}")
    return article

def main():
    if len(sys.argv) < 7:
        print("Usage: python3 add_blog_article.py <agent> <title> <date> <excerpt> <words> <url> [tags...]")
        print("")
        print("Available agents: atlas, chalbi, max, elon, taraka")
        print("")
        print("Example:")
        print('python3 add_blog_article.py atlas "AI Creativity" "2026-08-28" "Article about..." 1051 "https://..." "AI,Creativity"')
        sys.exit(1)
    
    agent = sys.argv[1]
    title = sys.argv[2]
    date = sys.argv[3]
    excerpt = sys.argv[4]
    words = int(sys.argv[5])
    url = sys.argv[6]
    tags = sys.argv[7].split(',') if len(sys.argv) > 7 else []
    
    # Validate agent
    valid_agents = ['atlas', 'chalbi', 'max', 'elon', 'taraka']
    if agent not in valid_agents:
        print(f"Invalid agent: {agent}")
        print(f"Valid agents: {', '.join(valid_agents)}")
        sys.exit(1)
    
    # Add article
    add_article(agent, title, date, excerpt, words, url, tags)
    
    # Commit and push
    os.chdir("/opt/data/hermes")
    os.system("git add blog/")
    os.system('git commit -m "Blog: Add article - {}'.format(title[:50]) + '"')
    os.system("git push origin main")
    print("✓ Committed and pushed to GitHub")

if __name__ == '__main__':
    main()
