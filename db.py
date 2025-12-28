import sqlite3

DB_NAME = "tasks.db"

def init_db():
    """Initialize the database and create tasks table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_text TEXT NOT NULL,
            due_date DATE NOT NULL,
            completed INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


def add_task(task_text, due_date):
    """Add a new task to the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task_text, due_date) VALUES (?, ?)", (task_text, due_date))
    conn.commit()
    conn.close()


def undo_last_task():
    """Delete the most recently added task."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM tasks ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    if row:
        c.execute("DELETE FROM tasks WHERE id = ?", (row[0],))
        conn.commit()
    conn.close()


from datetime import date

def carry_forward():
    """Move incomplete tasks from past dates to today."""
    today = date.today()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET due_date = ? WHERE due_date < ? AND completed = 0", (today, today))
    conn.commit()
    conn.close()


def list_today_tasks():
    """Return a list of incomplete tasks due today."""
    today = date.today()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, task_text FROM tasks WHERE due_date = ? AND completed = 0", (today,))
    rows = c.fetchall()
    conn.close()
    return rows


def get_today_pending_tasks(force):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    today = date.today().isoformat()

    if force:
        c.execute("""
            SELECT id, task_text FROM tasks
            WHERE due_date = ?
            AND completed = 0;
        """, (today,))
        rows = c.fetchall()
    else:
        c.execute("""
                    SELECT id, task_text FROM tasks
                    WHERE due_date = ?
                    AND completed = 0
                    AND (last_reminded IS NULL OR last_reminded != ?);
                """, (today, today))
        rows = c.fetchall()
    conn.close()
    return rows


def mark_reminded(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "UPDATE tasks SET last_reminded = ? WHERE id = ?",
        (date.today().isoformat(), task_id)
    )

    conn.commit()
    conn.close()


def mark_completed(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "UPDATE tasks SET completed = 1 WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


