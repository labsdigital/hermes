---
name: multi-agent-workflow
description: "Orchestrate Hermes agents with Kanban and blog integration."
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [multi-agent, workflow, orchestration]
---

# Multi-Agent Workflow

Pattern untuk mengoordinasikan beberapa agen Hermes.

## Artikel Production Pipeline

```
1. @max riset topik → JSON
2. @atlas pilih topik
3. @atlas tulis + ilustrasi
4. @atlas publish → GitHub + Blog
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `kanban_setup.py` | Init database |
| `setup_board.py` | Create workflow board |
| `update_dashboard.py` | Push to GitHub |
| `add_blog_article.py` | Add to blog |

## Dashboards
- Kanban: https://labsdigital.github.io/hermes/kanban-dashboard/
- Blog: https://labsdigital.github.io/hermes/blog/
