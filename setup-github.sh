#!/bin/bash
# Setup script for Kanban Dashboard

set -e

REPO_NAME="kanban-dashboard"
GITHUB_USERNAME="jasonckfan"

echo "🚀 Setting up Kanban Dashboard..."
echo ""

# Check if gh is installed and logged in
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) not found. Please install it first:"
    echo "   brew install gh"
    exit 1
fi

# Check if logged in
if ! gh auth status &> /dev/null; then
    echo "🔐 Please login to GitHub:"
    gh auth login
fi

# Get username
GITHUB_USERNAME=$(gh api user -q .login)
echo "✅ Logged in as: $GITHUB_USERNAME"

# Create repo if not exists
echo "📦 Creating GitHub repository..."
if gh repo view "$GITHUB_USERNAME/$REPO_NAME" &> /dev/null; then
    echo "✅ Repository already exists"
else
    gh repo create "$REPO_NAME" --public --description "Hermes Kanban Dashboard" --source=. --push
    echo "✅ Repository created"
fi

# Setup git remote
echo "🔗 Setting up git remote..."
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Push main branch
echo "📤 Pushing to main branch..."
git push -u origin main || echo "Main branch already pushed"

# Enable GitHub Pages
echo "🌐 Enabling GitHub Pages..."
gh api "repos/$GITHUB_USERNAME/$REPO_NAME/pages" \
    --method POST \
    --input - <<< '{"source":{"branch":"gh-pages","path":"/"}}' \
    2>/dev/null || echo "GitHub Pages may already be enabled"

echo ""
echo "✅ Setup complete!"
echo ""
echo "🌐 Your dashboard will be available at:"
echo "   https://$GITHUB_USERNAME.github.io/$REPO_NAME/"
echo ""
echo "📋 Next steps:"
echo "1. Run: python3 build-and-deploy.py"
echo "2. Wait 1-2 minutes for GitHub Pages to deploy"
echo "3. Visit the URL above"
