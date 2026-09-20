---
name: book-writing
description: Write multi-chapter books with cohesive arcs.
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [book, writing, nonfiction, chapters]
---

# Book Writing Pattern

Use when creating multi-chapter books or comprehensive long-form content.

## When to Use

- User requests a book with multiple chapters
- Creating comprehensive guides with progressive narrative
- Long-form content requiring structural planning

## Book Structure

```
book-name/
├── README.md
├── outline.md
└── chapters/
    ├── 01-title.md
    └── ...
```

## Requirements

| Aspect | Rule |
|--------|------|
| Word count | 1,500+ words/chapter |
| Perspective | Eagle view (third person) |
| Forbidden | aku, saya, ku- |
| Style | Harari-style nonfiction |
| Structure | Hook → Sections → Transisi |

## Workflow

### Phase 1: Planning
```bash
mkdir -p book-v2/chapters
```

1. Create README.md with ToC
2. Create outline.md with breakdowns
3. Verify cohesive arc

### Phase 2: Writing
For each chapter:
1. Write 1,500+ words
2. Use third person throughout
3. Include forward transitions
4. Reference earlier chapters

### Phase 3: Publishing
```bash
git add book-v2/
git commit -m "Book: <title>"
git push origin main
```

## Arc Structure Example

```
Part I: Foundation (Ch 1-2)
Part II: Understanding (Ch 3-5)
Part III: Impact (Ch 6-7)
Part IV: Dynamics (Ch 8-9)
Part V: Future (Ch 10-13)
```

## Cohesion Checklist

- [ ] Each chapter opens with concrete hook
- [ ] References earlier concepts (callbacks)
- [ ] Sets up later questions (foreshadowing)
- [ ] No first-person pronouns
- [ ] Transitions create forward momentum

## Pitfalls

### First Person Slip
Common error: using "aku" when explaining experience.
Fix: Rewrite as "Manusia" or rephrase.

### Island Chapters
Each chapter feels isolated.
Fix: Add cross-references in 3-5 places.

### Under-worded
Chapters below 1,500 words.
Fix: Expand examples and case studies.

## Quick Reference

| Task | Command |
|------|---------|
| Create folder | `mkdir -p book-v2/chapters` |
| Check word count | `wc -w chapters/*.md` |
| Verify no first person | `grep -c "aku\|saya" chapters/*.md` |
| Commit | `git add book-v2/ && git commit -m "..." && git push` |

## Related Skills
- `nonfiction-harari-style`
- `indonesian-tech-writing`
- `github-push-workflow`

## Session Example
"Manusia dan Mesin" (2026-08-26):
- 13 chapters, 5 parts
- ~13,460 words total
- GitHub: https://github.com/labsdigital/hermes/tree/main/book-v2