---
name: github-push-workflow
description: "Push to GitHub without gh CLI; handle merge conflicts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [GitHub, Git, Push, Workflow]
    related_skills: [github-repo-management]
---

# GitHub Push Workflow

Use when pushing files to GitHub without `gh` CLI or with merge conflicts.

## Prerequisites

- GitHub account with repo access
- PAT stored in `~/.git-credentials`
- Git installed

## Common Issues & Solutions

### Issue 1: `gh` command not found

Use raw `git` + `curl`:

```bash
TOKEN=$(grep github.com ~/.git-credentials | cut -d@ -f1 | cut -d: -f2)
```

### Issue 2: Unrelated histories

```bash
git pull origin main --allow-unrelated-histories
```

### Issue 3: Untracked file conflicts during merge

```bash
mv problematic_file /tmp/
git pull origin main --allow-unrelated-histories
mv /tmp/problematic_file .
```

### Issue 3b: Sibling subagent modified your target file (concurrent writes)

Multi-agent setups share one worktree. `write_file` may return a warning like:
`"<file>" was modified by sibling subagent '<id>' but this agent never read it.`
Do NOT blind-retry the write — the sibling may have landed real changes.

Fix:
```bash
read_file <target>             # inspect what's actually there now
git -C <repo> diff -- <path>   # see what changed vs HEAD
```
Then merge your content on top (re-read + targeted `patch`) or consciously
overwrite if the file was created FOR you this session. Before committing,
re-run `git status --short` and stage explicit paths only, so you never sweep a
sibling's in-flight changes into your commit.

### Issue 4: `fatal: Pathspec ... is in submodule 'X'`

The outer repo tracks your target folder as a submodule; the REAL repo (own
`.git`, own origin) is the subdirectory itself. Running `git add` from the
parent always fails with this error.

Fix: find the true repo root from inside the target directory, then operate
there:

```bash
cd <target-dir> && git rev-parse --show-toplevel   # prints the INNER repo path
git -C <inner-repo> add <your-file>
git -C <inner-repo> commit -m "..." && git -C <inner-repo> push
```

Real-world example: workspace root `/opt/data` treats `hermes/` as a submodule;
the actual article repo with origin `labsdigital/hermes.git` lives at
`/opt/data/hermes`.

### Issue 5: `nothing to commit, working tree clean` but your files exist

Some managed workspaces run auto-commit hooks (watchers/automation) that stage,
commit AND push new files the moment they land. If `git add` + `git commit`
reports nothing to commit while your files are on disk:

```bash
git log --oneline -3 -- <your-path>     # did a hook already commit it?
git rev-parse HEAD origin/main          # local tip vs remote tip
```

If HEAD == origin/main and your files show up in `git ls-files`, the work is
already committed and pushed — do NOT create an empty commit or re-push.
The auto-commit's message will differ from the one you intended, so verify it
actually contains YOUR file before reporting done:

```bash
git show --stat <sha>              # path + insertion count = your file?
git ls-tree origin/main <dir>/     # blob present on the pushed remote tip?
```

Real-world examples: writing `elon/svg-showcase/**` in `/opt/data/hermes`; a hook
landed commit `8e2a5c1` and pushed it before the agent's own `git commit` ran.
Again 2026-08-24: `elon/rangkaian-listrik-v2/index.html` (82 KB) landed as
commit `f11b47a` seconds after the write — confirmed via `git show --stat`
(1633 insertions, correct path) + `git ls-tree origin/main elon/rangkaian-listrik-v2/`.

## Pitfall: Never `git add .` in a Shared/Runtime Worktree

Agent workspaces accumulate dirty runtime files you must NOT commit: `.env`
(secrets!), gateway lock files, state/session JSONs, other agents' WIP. Always
survey first and stage explicit paths:

```bash
git status --short            # see what's dirty
git add <only-your-file.md>   # explicit staging, never blanket
git commit -m "..." && git push origin <branch>
```

## Quick Reference

| Task | Command |
|------|---------|
| Init repo | `git init && git branch -m main` |
| Add remote | `git remote add origin https://github.com/USER/REPO.git` |
| Pull with merge | `git pull origin main --allow-unrelated-histories` |
| Commit | `git status --short && git add <explicit-files> && git commit -m "message"` |
| Push | `git push origin main` |

## Verification

Verify BOTH that the file is tracked locally AND that the remote has your
commit — a swallowed or batched-away command can leave a false "success"
assumption:

```bash
git ls-files --error-unmatch <file>      # tracked locally
curl -s -o /dev/null -w "%{http_code}" \
  "https://api.github.com/repos/OWNER/REPO/contents/FILE.md?ref=main"   # expect 200
git rev-parse HEAD                       # local tip...
git ls-remote origin refs/heads/main     # ...must match remote tip
```

## Workflow Requirement: Always Include GitHub Pages URL

When pushing educational/web apps to `labsdigital/hermes`, ALWAYS include the
published GitHub Pages URL in both the commit message AND the response to user.

**Commit message format:**
```
Elon: [Project Name] - Feature description

GitHub: https://github.com/labsdigital/hermes/tree/main/<folder>
Pages: https://labsdigital.github.io/hermes/<folder>/
```

**Response format:**
```
🔗 GitHub: https://github.com/labsdigital/hermes/tree/main/<folder>
🌐 Pages: https://labsdigital.github.io/hermes/<folder>/
```

This applies to all `elon/` subagent work products committed to the main branch.
Even if GitHub Pages shows 404 initially (takes ~2-5 min to deploy), report the URL anyway — it will be live shortly.
