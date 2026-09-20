---
name: renaminG-subagent
description: "Rename subagent directory and update all references."
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [subagent, rename, refactoring]
---

# Rename Subagent Guide

Quick reference for renaming a subagent safely.

## Checklist
1. `mv hermes/old-name hermes/new-name`
2. `grep -r "old-name" hermes/new-name --include="*.md"` - Find all refs
3. Update: AGENTS.md, README.md, SKILL.md, nested docs
4. `git add -A && git commit -m "NewName: Rename from OldName"`
5. `git push origin main`

## Common Mistakes
- Forgetting nested references (e.g., voxel-builder/README.md)
- Not updating commit conventions
- Missing internal links