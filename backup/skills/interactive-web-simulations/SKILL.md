---
name: interactive-web-simulations
description: Create interactive web simulations for education.
version: 1.0.0
author: Hermes Agent + labsdigital
license: MIT
tags: [web, simulation, education, interactive, html, css, javascript]
---

# Interactive Web Simulations

Create standalone HTML/CSS/JS applications for educational simulations with modern, responsive design.

## When to Use

- User requests interactive math/science simulations
- Educational lab-style web apps needed
- Visual explanations of abstract concepts (ratios, percentages, physics)
- PhET-style interactive learning tools

## Tech Stack Defaults

```
Base: Single HTML file (no build step)
Styling: Modern CSS with variables for theming
Icons: Emoji or inline SVG
Fonts: Google Fonts (Inter, Poppins)
Animations: CSS transitions + requestAnimationFrame
State: Vanilla JS (no frameworks)
```

## Structure Pattern

```
project-name/
└── index.html          # Single-file app with embedded CSS/JS
```

Or for multi-file projects:
```
project-name/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── app.js
└── assets/
    └── icons/
```

## Design Principles

### 1. Dark/Light Mode
Always include a theme toggle. Use CSS custom properties:
```css
:root {
  --bg: #0f172a;
  --bg-card: #1e293b;
  --text: #f8fafc;
  --primary: #6366f1;
}
.light-mode {
  --bg: #f8fafc;
  --bg-card: #ffffff;
  --text: #0f172a;
}
```

### 2. Modern UI Components
- Card-based layout with hover effects
- Gradient accents
- Smooth transitions (0.3s ease)
- Box shadows for depth
- Rounded corners (border-radius: 15-20px)

### 3. Interactive Elements
- Range sliders with styled thumbs
- Real-time value display
- Visual feedback on interactions
- Animated transitions

### 4. Responsive Design
```css
.sim-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}
@media (max-width: 768px) {
  .sim-grid { grid-template-columns: 1fr; }
}
```

## Common Simulation Types

### Ratio & Proportion
- Color mixers (RGB blending)
- Scale converters (map scales)
- Recipe scalers
- Speed/distance calculators

### Percentage & Fraction
- Pie charts (CSS conic-gradient)
- Bar comparisons
- Decimal/fraction converters

### Physics/Motion
- Projectile motion (gravity, angle, velocity)
- Wave visualization
- Collision simulation
- Pendulum dynamics

### Circuit/Electricity
- Series/parallel circuits
- Ohm's law visualizer
- Resistor color code decoder

### Computational Thinking
- Decomposition trees (SVG interactive)
- Pattern recognition games
- Abstraction filtering
- Algorithm building (drag-drop ordering)
- Pendulum dynamics

### Circuit/Electricity
- Series/parallel circuits
- Ohm's law visualizer
- Resistor color code decoder

### Computational Thinking
- Decomposition trees (SVG interactive)
- Pattern recognition games
- Abstraction filtering
- Algorithm building (drag-drop ordering)

## File Output Location

Save to: `/opt/data/hermes/elon/<project-name>/index.html`

## Commit Pattern

```bash
cd /opt/data/hermes
git add elon/<project-name>/
git commit -m "Elon: [Project Name] - Interactive Simulation"
git push origin main
```

**Important:** Always include GitHub Pages URL in commit message and response:
```
🔗 GitHub: https://github.com/labsdigital/hermes/tree/main/elon/<project-name>
🌐 Pages: https://labsdigital.github.io/hermes/elon/<project-name>/
```

## Example: Color Mixer Simulation

```html
<!-- Key components -->
<div class="color-mixer">
  <div class="color-beaker">
    <div class="color-liquid" id="red" style="height: 60%; background: #ef4444;"></div>
  </div>
  <input type="range" id="red-slider" min="0" max="100" value="60">
</div>
<div class="mixed-result" id="mixed" style="background: rgb(180, 100, 50);"></div>
```

## JavaScript Pattern

```javascript
function updateSimulation() {
  const value = parseInt(document.getElementById('slider').value);
  document.getElementById('display').textContent = value;
  element.style.width = value + '%';
}
document.getElementById('slider').addEventListener('input', updateSimulation);
```

## Canvas Animation Best Practices

For physics simulations with canvas:
1. Set `canvas.width/height` BEFORE any draw calls
2. Use `(timestamp - lastTime) / 1000` for delta time (seconds)
3. Clamp delta to max 0.05s to prevent spiral on tab-switch
4. Call `requestAnimationFrame(loop)` at END of loop function
5. Store animation ID and cancel before restarting
6. Verify with: `typeof animId === 'number' && animId !== 0`

## Testing Checklist

- [ ] Works on mobile (responsive)
- [ ] Dark/light mode toggles correctly
- [ ] All sliders interact in real-time
- [ ] Animations are smooth (no jank)
- [ ] No console errors
- [ ] File size < 100KB (single HTML preferred)
- [ ] GitHub Pages URL included in commit/response

## Pitfalls

- Don't use external CDN dependencies unless requested
- Avoid complex frameworks - vanilla JS is preferred
- Test color mixing math carefully (RGB interpolation)
- Ensure animations use `transform` and `opacity` for performance
- **SVG mode**: Use svg-skill for static diagrams, visualise for interactive widgets
- **Gradient flashing**: Streaming doesn't support gradients — use flat fills
- **viewBox width**: Always 680px for visualise compatibility
- **EduApp2 style**: When user references EduApp2, use desktop-app shell (sidebar+topbar+light theme), NOT dark theme

## Related Skills

- `svg-skill` - Production-ready SVG markup (icons, logos, charts)
- `svg-education` - Educational SVG illustrations (science, math diagrams)
- `visualise` - Inline interactive visuals in conversations  
- `web-slide-decks` - Single-file HTML presentation decks
- `prd-generator` - Product Requirements Documents
- `interactive-html-apps` - Single-file interactive HTML web apps
