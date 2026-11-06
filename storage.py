import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DATA_DIR = Path.home() / ".buildpilot"
DB_PATH = DATA_DIR / "buildpilot.db"


def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT DEFAULT '',
                status TEXT DEFAULT 'active',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            );

            CREATE TABLE IF NOT EXISTS checkpoints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                summary TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY(project_id) REFERENCES projects(id)
            );
        """)


def add_project(name, description=""):
    if not name or not name.strip():
        raise ValueError("Project name cannot be empty")

    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO projects (name, description, created_at) VALUES (?, ?, ?)",
            (name.strip(), description, datetime.now(timezone.utc).isoformat())
        )
        return cursor.lastrowid


def list_projects():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM projects ORDER BY id DESC"
        ).fetchall()
        return [dict(row) for row in rows]


def add_task(project_id, title):
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    with get_connection() as conn:
        project = conn.execute(
            "SELECT id FROM projects WHERE id = ?", (project_id,)
        ).fetchone()

        if project is None:
            raise ValueError("Project not found")

        cursor = conn.execute(
            "INSERT INTO tasks (project_id, title, created_at) VALUES (?, ?, ?)",
            (project_id, title.strip(), datetime.now(timezone.utc).isoformat())
        )
        return cursor.lastrowid


def list_tasks(project_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE project_id = ? ORDER BY id DESC",
            (project_id,)
        ).fetchall()
        return [dict(row) for row in rows]


def update_task(task_id, status):
    allowed = {"pending", "in_progress", "completed"}

    if status not in allowed:
        raise ValueError(f"Status must be one of: {', '.join(sorted(allowed))}")

    with get_connection() as conn:
        cursor = conn.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )

        if cursor.rowcount == 0:
            raise ValueError("Task not found")


def add_checkpoint(project_id, summary):
    if not summary or not summary.strip():
        raise ValueError("Checkpoint summary cannot be empty")

    with get_connection() as conn:
        project = conn.execute(
            "SELECT id FROM projects WHERE id = ?", (project_id,)
        ).fetchone()

        if project is None:
            raise ValueError("Project not found")

        cursor = conn.execute(
            "INSERT INTO checkpoints (project_id, summary, created_at) VALUES (?, ?, ?)",
            (project_id, summary.strip(), datetime.now(timezone.utc).isoformat())
        )
        return cursor.lastrowid


def latest_checkpoint(project_id):
    with get_connection() as conn:
        row = conn.execute(
            """SELECT * FROM checkpoints
               WHERE project_id = ?
               ORDER BY id DESC LIMIT 1""",
            (project_id,)
        ).fetchone()

        return dict(row) if row else None
def get_project_context(project_id):
    with get_connection() as conn:
        project = conn.execute(
            "SELECT * FROM projects WHERE id = ?",
            (project_id,)
        ).fetchone()

        if project is None:
            raise ValueError("Project not found")

        tasks = conn.execute(
            "SELECT * FROM tasks WHERE project_id = ? ORDER BY id DESC",
            (project_id,)
        ).fetchall()

        checkpoint = conn.execute(
            """SELECT * FROM checkpoints
               WHERE project_id = ?
               ORDER BY id DESC LIMIT 1""",
            (project_id,)
        ).fetchone()

        return {
            "project": dict(project),
            "tasks": [dict(task) for task in tasks],
            "latest_checkpoint": dict(checkpoint) if checkpoint else None
        }
