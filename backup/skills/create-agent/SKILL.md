---
name: create-agent
description: Create Hermes subagent with AGENTS.md and push to GitHub.
---

# Create New Agent

## Directory Structure

```
/opt/data/hermes/<agent-name>/
├── AGENTS.md              # Agent character, persona, capabilities
├── skills/                # Skill files (.md)
├── references/            # Reference documents
├── reports/               # Generated output (articles, files)
└── images/                # Generated images
```

## AGENTS.md Template

```markdown
---
name: <agent-name>
description: >
  Brief description of agent purpose and trigger phrases.
---

# <Agent Name> — Agent Description

## Character & Persona
- Traits, communication style
- Focus areas

## Capabilities
1. Capability 1
2. Capability 2
3. Capability 3

## Workflow
Step-by-step process

## Output Format
Expected deliverables
```

## Required Files

1. **AGENTS.md** — Agent identity and behavior
2. **skills/*.md** — Core skill definitions
3. **references/*.md** — Supporting documents (download from taraka.id if provided)
4. **reports/** — Empty directory for output

## Push to GitHub

Always commit and push to GitHub after creation:

```bash
cd /opt/data/hermes
git add <agent-name>/
git commit -m "<Agent>: Add <agent-name> agent for <purpose>"
git push origin main
```

## Example: Creating @minerva

```bash
# 1. Create directory structure
mkdir -p /opt/data/hermes/minerva/{reports,images,skills,references}

# 2. Write AGENTS.md
write_file(path="/opt/data/hermes/minerva/AGENTS.md", content=...)

# 3. Download references from taraka.id
curl -s "https://taraka.id/AGENTS/?path=skills%2FSoal_Ujian%2F<file>&view=1" | sed 's/<[^>]*>//g' > <local-file>

# 4. Write skill files
write_file(path="/opt/data/hermes/minerva/skills/exam-preparation.md", content=...)

# 5. Commit and push
cd /opt/data/hermes && git add minerva/ && git commit -m "..." && git push origin main
```

## URL Pattern

- GitHub: https://github.com/labsdigital/hermes/tree/main/<agent-name>
- Blog (if applicable): https://labsdigital.github.io/hermes/blog/
- Dashboard: https://labsdigital.github.io/hermes/kanban/
