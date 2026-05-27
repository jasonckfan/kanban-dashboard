#!/usr/bin/env python3
"""
Build script for Hermes Kanban Dashboard
Reads from SQLite and generates static JSON for the dashboard
"""
import sqlite3
import json
import os
import sys
from datetime import datetime

KANBAN_DB = os.path.expanduser("~/.hermes/kanban.db")
OUTPUT_FILE = "kanban-data.js"

def get_db_connection():
    """Connect to kanban database"""
    if not os.path.exists(KANBAN_DB):
        print(f"Error: Kanban database not found at {KANBAN_DB}")
        sys.exit(1)
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
        # Boards table might not exist
        return [{"slug": "default", "name": "Default", "description": "Default board"}]

def generate_js(tasks, boards):
    """Generate JavaScript file with embedded data"""
    data = {
        "tasks": tasks,
        "boards": boards,
        "generated_at": datetime.now().isoformat()
    }
    
    js_content = f"""// Auto-generated Kanban data
// Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const KANBAN_DATA = {json.dumps(data, indent=2, ensure_ascii=False)};

// Override the data in the dashboard
if (typeof window !== 'undefined') {{
    window.KANBAN_DATA = KANBAN_DATA;
    if (typeof renderTasks === 'function') {{
        renderTasks();
    }}
}}
"""
    return js_content

def main():
    print("🔍 Reading kanban database...")
    conn = get_db_connection()
    
    print("📋 Fetching tasks...")
    tasks = fetch_tasks(conn)
    
    print("📊 Fetching boards...")
    boards = fetch_boards(conn)
    
    conn.close()
    
    print(f"✅ Found {len(tasks)} tasks, {len(boards)} boards")
    
    print(f"📝 Generating {OUTPUT_FILE}...")
    js_content = generate_js(tasks, boards)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    print(f"✅ Done! Output: {os.path.abspath(OUTPUT_FILE)}")
    print(f"\nNext steps:")
    print("1. Include kanban-data.js in your index.html")
    print("2. Deploy to GitHub Pages")

if __name__ == "__main__":
    main()
