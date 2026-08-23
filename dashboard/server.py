#!/usr/bin/env python3
"""Hermes Agent Dashboard - Real-time monitoring server"""

import json
import subprocess
import sqlite3
import os
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__, static_folder='static')

HERMES_PATH = '/opt/data/hermes'
AIRTABLE_TOKEN = os.getenv('AIRTABLE_API_KEY', '')
AIRTABLE_BASE = 'appHDwcERrnRH02YS'
AIRTABLE_TABLE = 'tblExdQkNbL9bZbgQ'

def get_git_log(limit=20):
    """Get recent git commits"""
    try:
        result = subprocess.run(
            ['git', '-C', HERMES_PATH, 'log', '--oneline', f'-n{limit}'],
            capture_output=True, text=True, timeout=10
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(' ', 1)
                commits.append({
                    'hash': parts[0],
                    'message': parts[1] if len(parts) > 1 else ''
                })
        return commits
    except:
        return []

def get_agent_stats():
    """Get statistics for each subagent"""
    agents = {
        'max': {'articles': 0, 'path': 'max/reports'},
        'elon': {'articles': 0, 'path': 'elon'},
        'chalbi': {'articles': 0, 'path': 'chalbi/reports'},
        'taraka': {'proposals': 0, 'path': 'taraka/proposals'}
    }
    
    for agent, data in agents.items():
        path = os.path.join(HERMES_PATH, data['path'])
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.endswith('.md')]
            data['articles'] = len(files)
    
    return agents

def get_airtable_count():
    """Get article count from Airtable"""
    if not AIRTABLE_TOKEN:
        return None
    try:
        url = f'https://api.airtable.com/v0/{AIRTABLE_BASE}/{AIRTABLE_TABLE}'
        headers = {'Authorization': f'Bearer {AIRTABLE_TOKEN}'}
        resp = requests.get(url, headers=headers, params={'pageSize': 1}, timeout=10)
        if resp.status_code == 200:
            return resp.json().get('totalRecords', 0)
    except:
        pass
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/agents')
def api_agents():
    return jsonify(get_agent_stats())

@app.route('/api/activity')
def api_activity():
    return jsonify(get_git_log(20))

@app.route('/api/airtable')
def api_airtable():
    return jsonify({'count': get_airtable_count()})

@app.route('/api/health')
def api_health():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'git_repo': os.path.exists(os.path.join(HERMES_PATH, '.git'))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)