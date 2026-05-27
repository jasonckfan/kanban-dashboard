// Auto-generated Kanban data
// Generated: 2026-05-27 20:18:37

const KANBAN_DATA = {
  "tasks": [],
  "boards": [
    {
      "slug": "default",
      "name": "Default",
      "description": "Default board"
    }
  ],
  "generated_at": "2026-05-27T20:18:37.809974"
};

// Override the data in the dashboard
if (typeof window !== 'undefined') {
    window.KANBAN_DATA = KANBAN_DATA;
    if (typeof renderTasks === 'function') {
        renderTasks();
    }
}
