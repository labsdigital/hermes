---
name: multi-subagent-orchestration
description: "Manage multiple specialized subagents in shared Hermes repo."
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [subagent, orchestration, multi-agent, naming, routing]
---

# Multi-Subagent Orchestration Pattern

Manage multiple specialized subagents working in parallel in a shared Hermes repository.

## When to Use
- Project requires 2+ specialized agents
- Each agent has distinct domain expertise
- Agents share repository but work independently
- Need clear routing protocol for user requests

## Architecture Pattern

```
hermes/
├── AGENTS.md              # Main agent profile (@zetta)
├── max/                   # AI news researcher
│   ├── AGENTS.md
│   ├── reports/
│   └── skills/
├── elon/                  # Web developer (renamed from mark)
│   ├── AGENTS.md
│   ├── voxel-builder/
│   └── skills/
├── chalbi/                # Rumi scholar
│   ├── AGENTS.md
│   ├── scripts/
│   └── reports/
└── taraka/                # Foundation manager
    ├── AGENTS.md
    ├── proposals/
    └── skills/
```

## Naming Convention (Critical)
Use DISTINCTIVE names to avoid confusion:

| Bad Examples | Good Examples |
|-------------|---------------|
| mark → max (too similar) | elon (distinctive) |
| alex → max (similar sound) | taraka (unique) |
| bob → rob (rhyme) | chalbi (memorable) |

**Rule**: If two names sound similar, rename the older one first.

## Chalbi Article Writing Style (Corrected 2026-08-22)

When writing Rumi/Masnavi articles for @chalbi, include:
1. **Original Persian/Arabic quotes** (kutipan asli) - REQUIRED
2. **Translation** (terjemahan Bahasa Indonesia)
3. **Elaboration** (makna & konteks)

Format:
```markdown
### Kutipan Penting
> [Teks Persia/Arab asli]
> — Masnavi, Daftar X, Beyt Y

**Terjemahan:**
[Terjemahan Bahasa Indonesia]

**Makna & Konteks:**
[Elaborasi mendalam]
```

**Before (WRONG):** Just narrative without Persian quotes
**After (CORRECT):** Persian quote → Translation → Elaboration

## Routing Protocol

Map user commands to subagent domains:

```
@max → AI news research & article writing
@elon → Web development, UI/UX, coding projects
@chalbi → Rumi/Masnavi studies, Persian literature
@taraka → Foundation proposals, event planning, grants
```

## Subagent Creation Workflow

### Step 1: Initialize
```bash
mkdir -p hermes/<name>/{reports,skills/domain-specific}
touch hermes/<name>/AGENTS.md
touch hermes/<name>/README.md
```

### Step 2: Write AGENTS.md
Include:
- Nama & peran
- Bahasa (default: Indonesia)
- Keahlian 3-5 poin
- Workflow langkah demi langkah
- Commit convention

### Step 3: Commit
```bash
cd /opt/data/hermes
git add <name>/
git commit -m "<Name>: Init subagent untuk [domain]"
git push origin main
```

## Renaming Subagent (Critical Operation)

When renaming (e.g., mark → elon):

```bash
# 1. Rename directory
mv hermes/mark hermes/elon

# 2. Find ALL references
grep -r "mark" hermes/elon --include="*.md" --include="*.sh"

# 3. Update files:
#    - AGENTS.md (all name references)
#    - README.md (links and description)
#    - SKILL.md (paths and examples)
#    - Any internal docs (e.g., voxel-builder/README.md)

# 4. Commit
git add -A
git commit -m "Elon: Rename subagent from Mark to Elon"
git push origin main
```

**Pitfall**: Always grep recursively before committing!

## Communication Patterns

### Direct Delegation
User explicitly calls subagent:
```
@max tulis tentang AI
@elon buatkan dashboard
@chalbi apa kata Rumi tentang cinta
@taraka buat proposal workshop
```

### Implicit Routing
Main agent (@zetta) routes based on context:
- Topic mentions "AI news" → route to @max
- Topic mentions "website/app" → route to @elon
- Topic mentions "Rumi/puisi" → route to @chalbi
- Topic mentions "proposal/foundation" → route to @taraka

## State Management

### Each Subagent Owns
- Its own directory
- Its own git history (commits)
- Its own skills and templates
- Its own output (reports, proposals, code)

### Shared Resources
- Repository root (.gitignore, config)
- Common scripts (if any)
- Documentation standards

## Best Practices

1. **Start with clear naming** - Avoid future rename pain
2. **Document routing** - Users should know who to call
3. **Limit to 4-6 subagents** - More creates confusion
4. **Regular cleanup** - Archive unused subagents
5. **Consistent structure** - All subagents follow same pattern

## Dashboard Integration (2026-08-22)

For monitoring subagents, deploy a dashboard:

### Static Dashboard (GitHub Pages)
Recommended for public access without server maintenance:
```bash
# Create folder in hermes repo
mkdir -p hermes/hermes-dashboard
# Add index.html with embedded JSON data
# Commit and push to GitHub
git add hermes/hermes-dashboard/
git commit -m "Dashboard: Add static monitoring"
git push origin main
# Enable GitHub Pages: Settings → Pages → Source: main, folder: /hermes-dashboard
```

### Real-time Dashboard (Node.js)
For internal use with live updates:
```bash
cd /opt/data/hermes-dashboard
node server.js
# Access locally: http://localhost:8080
# For external access, use SSH tunnel:
# ssh -L 8080:localhost:8080 hermes@103.153.189.177
```

**Note**: Container network isolation prevents direct external access. Use SSH tunnel or GitHub Pages.

See `dashboard-pattern` and `dashboard-network` skills for details.

## Common Pitfalls

| Pitfall | Solution |
|---------|----------|
| Similar names (mark/max) | Rename immediately, use grep to verify |
| Missing references after rename | Always grep -r before committing |
| Overlapping responsibilities | Document clear domain boundaries |
| Too many subagents | Max 5-6, archive unused ones |
| Inconsistent structure | Use template, enforce standards |

## Example: @zetta as Main Agent

Main agent (@zetta) orchestrates:
- Receives all user requests
- Routes to appropriate subagent
- Consolidates outputs if needed
- Maintains overall project vision

## Kanban Workflow Pattern

Untuk workflow multi-tahap dengan tracking status:

### Setup Board
```bash
# 1. Inisialisasi database
python3 /opt/data/hermes/scripts/kanban_setup.py

# 2. Tambah board baru dengan tasks
python3 /opt/data/hermes/scripts/setup_board.py
```

### CLI Commands
```bash
# List semua boards
python3 /opt/data/hermes/scripts/kanban_cli.py list

# Show board dengan tasks
python3 /opt/data/hermes/scripts/kanban_cli.py show <board_id>

# Create task baru
python3 /opt/data/hermes/scripts/kanban_cli.py create \
  --title "Judul Task" \
  --board <id> \
  --priority high/medium/low \
  --assignee <profile_name>

# Update status
python3 /opt/data/hermes/scripts/kanban_cli.py complete <task_id>
python3 /opt/data/hermes/scripts/kanban_cli.py block <task_id> --reason "Alasan"
python3 /opt/data/hermes/scripts/kanban_cli.py unblock <task_id>

# Stats
python3 /opt/data/hermes/scripts/kanban_cli.py stats
```

### Workflow Example: Artikel Creation
1. **Task 1** (@max): Riset topik → Todo → In Progress → Done
2. **Task 2** (@atlas): Pilih topik → Todo → In Progress → Done
3. **Task 3** (@atlas): Tulis artikel + ilustrasi → Todo → In Progress → Done
4. **Task 4** (@atlas): Publish GitHub/FTP/Email → Todo → In Progress → Done

**Database**: `/opt/data/home/.hermes/kanban.db`
**Scripts**: `/opt/data/hermes/scripts/`

**Pitfall**: Gunakan path absolut `/opt/data/home/.hermes/` bukan `$HOME/.hermes` karena container environment berbeda.

## Related Skills
- `subagent-creation` - Create new subagents
- `foundation-proposals` - For @taraka workflows
- `github-push-workflow` - Version control patterns
- `dashboard-pattern` - Dashboard deployment (static GitHub Pages & real-time Node.js)
- `dashboard-network` - Troubleshooting container network issues
- `subagent-model-configuration` - Per-subagent model setup (OpenRouter)