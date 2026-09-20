---
name: svg-education
description: Create educational SVG illustrations for learning materials.
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [svg, education, illustration, diagram, learning]
metadata:
  hermes:
    tags: [svg, education, illustration, diagram, learning]
    related_skills: [svg-skill, visualise, interactive-web-simulations]
---

# SVG Educational Illustrations

Create production-ready SVG illustrations for educational content.
Flat design style, max 4 colors, Indonesian labels, accessibility-first.

## When to Use

Use this skill when:
- Creating educational diagrams (science, math, biology, geography)
- Building illustrated learning materials for students
- Making visual explanations for topics like:
  - Biology: pencernaan, fotosintesis, tata surya
  - Math: pecahan, geometri, aljabar, statistik
  - Science: siklus air, energi, materi
  - Geography: peta, iklim, lapisan bumi

## Prerequisites

Ensure these skills are available:
- `svg-skill` - For SVG markup patterns
- `visualise` - For interactive HTML widgets (optional)

Load them before starting:
```
skill_view(name='svg-skill')
skill_view(name='visualise')
```

## Design System

### Color Palette (Education Theme)
```
Primary:
  --biru: #3B82F6      (blue - water, sky, info)
  --hijau: #10B981     (green - nature, plants, success)
  --kuning: #F59E0B    (amber - sun, energy, warning)
  --merah: #EF4444     (red - danger, important)

Neutral:
  --abu: #6B7280       (gray - text, borders)
  --gelap: #1F2937     (dark - text)
  --putih: #FFFFFF     (white - backgrounds)
```

### Style Rules
- **Flat design** - No gradients, no shadows (except simple fills)
- **Max 4 colors** per illustration
- **Simple shapes** - circles, rects, paths, polygons
- **Clear labels** - Bahasa Indonesia, readable fonts
- **viewBox** - Appropriate for content (200×200 to 600×400)

## Workflow

```
1. [ ] Define topic and learning objective
2. [ ] Choose viewBox and color palette
3. [ ] Sketch components (shapes, labels, arrows)
4. [ ] Write SVG markup with <title> and <desc>
5. [ ] Add Indonesian labels
6. [ ] Validate with svg-skill validate.sh
7. [ ] Test in browser
```

## Common Educational Topics

### Science Diagrams
| Topic | viewBox | Key Elements | Colors |
|-------|---------|--------------|--------|
| Siklus Air | 400×300 | matahari, awan, gunung, laut, panah | biru, kuning, hijau, abu |
| Fotosintesis | 400×300 | daun, sinar, CO₂, O₂, glukosa | hijau, biru, kuning |
| Sistem Pencernaan | 300×500 | mulut, kerongkongan, lambung, usus | merah, pink, oranye |
| Tata Surya | 600×400 | matahari, orbit, 8 planet | kuning, abu, biru, merah |

### Math Diagrams
| Topic | viewBox | Key Elements | Colors |
|-------|---------|--------------|--------|
| Pecahan | 400×200 | lingkaran terbagi, label | oranye, biru, hijau |
| Pythagoras | 400×300 | segitiga, persegi di sisi | oranye, biru, hijau |
| Segi Banyak | 300×300 | polygon, sudut, sisi | varias |
| Statistik | 400×300 | bar chart, line chart | varias |

## SVG Structure Template

```svg
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" 
     viewBox="0 0 400 300" 
     role="img" 
     aria-labelledby="title desc">
  <title id="title">Judul Ilustrasi</title>
  <desc id="desc">Penjelasan singkat untuk aksesibilitas.</desc>
  
  <!-- Background -->
  <rect width="400" height="300" fill="#F8FAFC"/>
  
  <!-- Main elements -->
  <g id="components">
    <!-- Shapes here -->
  </g>
  
  <!-- Labels -->
  <g id="labels" font-family="Inter, sans-serif" font-size="14">
    <text x="50" y="50">Label 1</text>
  </g>
</svg>
```

## Validation Checklist

- [ ] `xmlns="http://www.w3.org/2000/svg"` present
- [ ] `viewBox` set appropriately
- [ ] `<title>` and `<desc>` for accessibility
- [ ] UTF-8 declaration for Indonesian text
- [ ] Max 4 colors used
- [ ] No gradients (flat design)
- [ ] Labels readable at target size
- [ ] File validates: `bash /opt/data/skills/svg-skill/scripts/validate.sh file.svg`

## Output Locations

### Standalone SVG Files
Save to:
```
/opt/data/hermes/elon/education-svg/
```

### Inline SVG in HTML (Interactive)
Save to:
```
/opt/data/hermes/elon/education-inline/
```

Inline SVG = `<svg>...</svg>` directly inside HTML file (not `<img src="file.svg">`).
Benefits: CSS interactivity, hover effects, animations, easier embedding.

### Gallery/Index Page
Always create `index.html` when building multiple illustrations:
```
/opt/data/hermes/elon/education-inline/index.html
/opt/data/hermes/elon/education-svg/index.html
```

## Building Showcase Page

Create `index.html` with:
- Grid layout showing all illustrations
- Each illustration in a card with title
- Category badges (Sains, Matematika)
- Responsive design

Example card:
```html
<div class="card">
  <img src="siklus-air.svg" alt="Ilustrasi Siklus Air">
  <h3>Siklus Air</h3>
  <span class="badge sains">Sains</span>
  <p>Evaporasi, kondensasi, presipitasi</p>
</div>
```

## Examples Reference

### Standalone SVG Files
- `/opt/data/hermes/elon/education-svg/siklus-air.svg`
- `/opt/data/hermes/elon/education-svg/tata-surya.svg`
- `/opt/data/hermes/elon/education-svg/pecahan.svg`

### Inline SVG (HTML)
- `/opt/data/hermes/elon/education-inline/sel-tumbuhan.html`
- `/opt/data/hermes/elon/education-inline/listrik-sederhana.html`
- `/opt/data/hermes/elon/education-inline/bangun-datar.html`

## Pitfalls

- **Too detailed** - Keep shapes simple; educational SVGs should be clear at small sizes
- **Too many colors** - Max 4 colors maintains visual clarity
- **Missing labels** - Always add Indonesian text labels
- **Forgetting accessibility** - Include `<title>` and `<desc>`
- **Complex gradients** - Use flat fills for better scaling and print
- **Using external images** - Prefer inline SVG over `<img>` for interactivity
- **Not creating index.html** - Always create gallery page for multiple illustrations
- **Forgetting UTF-8** - Add XML declaration for non-ASCII text (Bahasa Indonesia)

## Related Skills

- `svg-skill` - Core SVG patterns and validation
- `visualise` - Interactive HTML widgets
- `web-slide-decks` - Presentation integration
