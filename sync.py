#!/usr/bin/env python3
"""
Sync Hermes Kanban to GitHub Pages
Reads from local SQLite and pushes to GitHub for static hosting
"""
import sqlite3
import json
import os
import subprocess
import shutil
from datetime import datetime

KANBAN_DB = os.path.expanduser("~/.hermes/kanban.db")
DASHBOARD_DIR = os.path.expanduser("~/kanban-dashboard")

def get_db_connection():
    """Connect to kanban database"""
    if not os.path.exists(KANBAN_DB):
        print(f"❌ Kanban database not found at {KANBAN_DB}")
        return None
    return sqlite3.connect(KANBAN_DB)

def fetch_tasks(conn):
    """Fetch all tasks from database"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id, title, body, assignee, status, priority,
            created_by, created_at, started_at, completed_at,
            workspace_kind, workspace_path, result
        FROM tasks
        ORDER BY created_at DESC
    """)
    
    tasks = []
    for row in cursor.fetchall():
        task = {
            "id": row[0],
            "title": row[1] or "Untitled",
            "body": row[2] or "",
            "assignee": row[3],
            "status": row[4] or "todo",
            "priority": row[5] or 0,
            "created_by": row[6],
            "created_at": row[7],
            "started_at": row[8],
            "completed_at": row[9],
            "workspace_kind": row[10],
            "workspace_path": row[11],
            "result": row[12]
        }
        tasks.append(task)
    
    return tasks

def fetch_boards(conn):
    """Fetch all boards"""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT slug, name, description FROM boards")
        boards = []
        for row in cursor.fetchall():
            boards.append({
                "slug": row[0],
                "name": row[1],
                "description": row[2]
            })
        return boards
    except sqlite3.OperationalError:
        return [{"slug": "default", "name": "Default", "description": "Default board"}]

def generate_data(tasks, boards):
    """Generate JSON data for dashboard"""
    return {
        "tasks": tasks,
        "boards": boards,
        "generated_at": datetime.now().isoformat(),
        "source": "hermes-kanban"
    }

def deploy_to_github():
    """Deploy to GitHub Pages"""
    os.chdir(DASHBOARD_DIR)
    
    # Switch to gh-pages branch
    result = subprocess.run(['git', 'checkout', 'gh-pages'], 
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Failed to checkout gh-pages: {result.stderr}")
        return False
    
    # Pull latest
    subprocess.run(['git', 'pull', 'origin', 'gh-pages'], 
                 capture_output=True)
    
    # Stage changes
    subprocess.run(['git', 'add', 'kanban-data.js'], check=True)
    
    # Check if there are changes
    result = subprocess.run(['git', 'diff', '--cached', '--quiet'])
    if result.returncode == 0:
        print("ℹ️  No changes to deploy")
        subprocess.run(['git', 'checkout', 'main'], capture_output=True)
        return True
    
    # Commit
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    result = subprocess.run(['git', 'commit', '-m', f'Update kanban data - {timestamp}'],
                          capture_output=True, text=True)
    
    # Push
    result = subprocess.run(['git', 'push', 'origin', 'gh-pages'],
                          capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Push failed: {result.stderr}")
        subprocess.run(['git', 'checkout', 'main'], capture_output=True)
        return False
    
    # Switch back to main
    subprocess.run(['git', 'checkout', 'main'], capture_output=True)
    
    return True

def main():
    print("🔄 Syncing Hermes Kanban to GitHub Pages...")
    print(f"📊 Database: {KANBAN_DB}")
    print(f"🌐 Dashboard: {DASHBOARD_DIR}")
    print()
    
    # Connect to database
    conn = get_db_connection()
    if not conn:
        print("❌ Cannot connect to kanban database")
        return 1
    
    try:
        # Fetch data
        print("📋 Fetching tasks...")
        tasks = fetch_tasks(conn)
        print(f"   Found {len(tasks)} tasks")
        
        print("📊 Fetching boards...")
        boards = fetch_boards(conn)
        print(f"   Found {len(boards)} boards")
        
        # Generate data
        data = generate_data(tasks, boards)
        
        # Write to file
        data_file = os.path.join(DASHBOARD_DIR, 'kanban-data.js')
        with open(data_file, 'w', encoding='utf-8') as f:
            f.write(f"const KANBAN_DATA = {json.dumps(data, indent=2, ensure_ascii=False)};")
        print(f"✅ Generated: {data_file}")
        
        # Deploy
        print("\n🚀 Deploying to GitHub Pages...")
        if deploy_to_github():
            print("✅ Deployed successfully!")
            print(f"\n🌐 Your dashboard: https://jasonckfan.github.io/kanban-dashboard/")
            print(f"📝 Tasks: {len(tasks)}")
            print(f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("❌ Deployment failed")
            return 1
            
    finally:
        conn.close()
    
    return 0

if __name__ == "__main__":
    exit(main())
