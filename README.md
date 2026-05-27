# Hermes Kanban Dashboard

A beautiful static dashboard for Hermes Kanban tasks, deployable to GitHub Pages.

## Features

- 📊 Kanban board view (To Do / In Progress / Done / Blocked)
- 📈 Statistics cards
- 📋 Task table with details
- 🎨 Modern Tailwind CSS design
- 📱 Responsive layout
- ⚡ Auto-refresh support

## Setup

### 1. Create GitHub Repository

Create a new repository on GitHub (e.g., `yourusername/kanban-dashboard`)

### 2. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/kanban-dashboard.git
git push -u origin main
```

### 3. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `gh-pages` / `main`
4. Click Save

### 4. Configure Database Sync (Important!)

The dashboard needs access to your `~/.hermes/kanban.db` file. Choose one method:

#### Option A: Manual Update
```bash
# Copy your kanban.db to the repo
cp ~/.hermes/kanban.db ./
python build.py
git add kanban-data.js
git commit -m "Update dashboard"
git push
```

#### Option B: Automated Sync (Advanced)
Set up a sync service to push your kanban.db to the repo automatically.

## File Structure

```
kanban-dashboard/
├── index.html          # Main dashboard
├── build.py           # Build script (generates kanban-data.js)
├── kanban-data.js     # Generated data file
├── .github/
│   └── workflows/
│       └── update-dashboard.yml  # GitHub Actions workflow
└── README.md
```

## Development

### Local Preview

```bash
python build.py
python -m http.server 8000
# Open http://localhost:8000
```

### Rebuild Data

```bash
python build.py
```

## Customization

Edit `index.html` to customize:
- Colors and themes
- Layout
- Additional columns
- Charts and graphs

## License

MIT
