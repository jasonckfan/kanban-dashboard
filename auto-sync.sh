#!/bin/bash
# Auto-sync Hermes Kanban to GitHub Pages
# Run this on your Mac to keep dashboard updated

echo "🔄 Hermes Kanban Auto-Sync"
echo "=========================="
echo ""

# Check if running from kanban-dashboard directory
if [ ! -f "sync.py" ]; then
    echo "❌ Please run from ~/kanban-dashboard directory"
    exit 1
fi

# Run sync
python3 sync.py

# Optional: Set up cron job
if [ "$1" == "--install-cron" ]; then
    echo ""
    echo "📅 Installing cron job (runs every 5 minutes)..."
    
    # Get current directory
    DASHBOARD_DIR="$(pwd)"
    
    # Create cron entry
    CRON_ENTRY="*/5 * * * * cd $DASHBOARD_DIR && python3 sync.py >> /tmp/kanban-sync.log 2>&1"
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -
    
    echo "✅ Cron job installed"
    echo "   Runs every 5 minutes"
    echo "   Log: /tmp/kanban-sync.log"
    echo ""
    echo "To remove: crontab -e and delete the line"
fi

echo ""
echo "💡 Tips:"
echo "   - Run manually: ./auto-sync.sh"
echo "   - Install auto-sync: ./auto-sync.sh --install-cron"
echo "   - View log: tail -f /tmp/kanban-sync.log"
