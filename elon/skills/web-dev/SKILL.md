# Skill: Web App Development

## Description
Membuat aplikasi web modern berbasis HTML, CSS, dan JavaScript. Fokus pada clean code, responsive design, dan good UX.

## Trigger
Gunakan skill ini ketika user meminta:
- Membuat aplikasi web
- Dashboard atau monitoring panel
- Landing page
- CRUD application
- Data visualization
- Tools atau utilities berbasis web
-任何形式的web前端开发

## Steps

### 1. Requirement Analysis
- Pahami kebutuhan user (fitur, target user, platform)
- Tentukan scope (single page vs multi page)
- Identifikasi dependencies (libraries, APIs)

### 2. Architecture Planning
```
Folder Structure:
mark/[project-name]/
├── index.html
├── css/
│   └── styles.css (optional)
├── js/
│   └── app.js
├── assets/
│   └── [images/icons]
└── README.md
```

### 3. Development Guidelines

#### HTML Structure
```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[App Name]</title>
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Custom CSS -->
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <!-- Content -->
    <script src="js/app.js"></script>
</body>
</html>
```

#### CSS Best Practices
- Use CSS Variables untuk theming
- Mobile-first responsive design
- Flexbox/Grid untuk layouts
- Smooth transitions & animations
- Clean, consistent spacing

#### JavaScript Patterns
- Module pattern atau IIFE
- Event delegation untuk dynamic elements
- Async/await untuk API calls
- Error handling dengan try/catch
- LocalStorage untuk persistence

### 4. UI Components Library
Buat reusable components:
- Cards
- Buttons
- Forms
- Modals
- Tables
- Charts
- Navigation

### 5. Testing Checklist
- [ ] Cross-browser compatible (Chrome, Firefox, Safari, Edge)
- [ ] Responsive on mobile/tablet/desktop
- [ ] All interactive elements work
- [ ] Error states handled
- [ ] Loading states shown
- [ ] Performance optimized
- [ ] Accessible (keyboard navigation, ARIA)

### 6. Deployment
- Push ke GitHub: `mark/` folder
- Enable GitHub Pages di settings
- Provide URL: `https://labsdigital.github.io/hermes/mark/[project-name]/`

### 7. Documentation
Write README.md dengan:
- Deskripsi aplikasi
- Features list
- Screenshot/GIF
- How to use
- Tech stack
- Deployment info

## Output Format
Single comprehensive HTML file dengan embedded CSS & JS (untuk simple apps), atau organized folder structure (untuk complex apps).

## Examples

### Simple App (Single File)
```
mark/todo-app/index.html
- Embedded CSS in <style>
- Embedded JS in <script>
- CDN for libraries
- Ready to open in browser
```

### Complex App (Multi File)
```
mark/dashboard/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── app.js
├── assets/
│   └── logo.svg
└── README.md
```

## Libraries推荐

### Essential (CDN)
- Font Awesome: Icons
- Google Fonts: Inter, Poppins
- Chart.js: Charts (jika perlu)
- ApexCharts: Advanced charts (optional)

### Optional (jika diminta)
- React/Vue: Untuk complex state management
- Tailwind CSS: Utility-first styling
- Alpine.js: Lightweight reactivity
- GSAP: Advanced animations

## Quality Standards
- Code must be clean and well-commented
- UI must be modern and professional
- Must be fully functional (no broken features)
- Responsive on all screen sizes
- Accessible (WCAG 2.1 AA minimum)

## Common Patterns

### Local Storage Manager
```javascript
const Storage = {
    get(key) { return JSON.parse(localStorage.getItem(key) || '[]'); },
    set(key, data) { localStorage.setItem(key, JSON.stringify(data)); },
    remove(key) { localStorage.removeItem(key); }
};
```

### API Fetch Helper
```javascript
async function fetchData(url) {
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('Network error');
        return await res.json();
    } catch (err) {
        console.error('Fetch error:', err);
        return null;
    }
}
```

### Modal Component
```javascript
function openModal(id) {
    document.getElementById(id).classList.add('active');
}
function closeModal(id) {
    document.getElementById(id).classList.remove('active');
}
```

## Notes
- Always test before committing
- Use semantic HTML
- Optimize for performance
- Provide clear documentation
- Make it deployable immediately
