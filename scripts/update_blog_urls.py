#!/usr/bin/env python3
"""
Update blog article URLs from raw GitHub to blob GitHub format
"""
import json
import os
import glob

BLOG_DIR = "/opt/data/hermes/blog"

def update_url(old_url):
    """Convert raw GitHub URL to blob GitHub URL"""
    # raw.githubusercontent.com -> github.com/labsdigital/hermes/blob/main
    if "raw.githubusercontent.com" in old_url:
        # Extract path after main/
        parts = old_url.split("/main/")
        if len(parts) == 2:
            filename = parts[1]
            return f"https://github.com/labsdigital/hermes/blob/main/{filename}"
    return old_url

def update_agent_articles(agent_dir):
    """Update articles for one agent"""
    articles_file = os.path.join(agent_dir, "articles.json")
    
    if not os.path.exists(articles_file):
        return 0
    
    with open(articles_file, 'r') as f:
        articles = json.load(f)
    
    updated = 0
    for article in articles:
        old_url = article.get('url', '')
        new_url = update_url(old_url)
        if old_url != new_url:
            article['url'] = new_url
            updated += 1
    
    if updated > 0:
        with open(articles_file, 'w') as f:
            json.dump(articles, f, indent=2)
    
    return updated

def main():
    total_updated = 0
    
    # Update all agent articles
    for agent_dir in glob.glob(os.path.join(BLOG_DIR, "*/")):
        agent_name = os.path.basename(agent_dir.rstrip('/'))
        updated = update_agent_articles(agent_dir)
        if updated > 0:
            print(f"✓ {agent_name}: Updated {updated} URLs")
            total_updated += updated
    
    print(f"\nTotal updated: {total_updated} URLs")
    return total_updated

if __name__ == '__main__':
    main()
