# backend/database.py
import sqlite3

DB_PATH = "life_manager.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def execute_sql(conn, name, sql):
    try:
        print(f"\nRunning SQL block: {name}")
        print(sql)
        conn.execute(sql)
        print(f"Success: {name}")
    except sqlite3.Error as e:
        print(f"\nDB ERROR in: {name}")
        print(f"SQLite said: {e}")
        print("\nSQL that failed:")
        print(sql)
        raise

def init_db():
    with get_conn() as conn:
        goals_sql = """
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL,
            due TEXT NOT NULL,
            action TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
        """

        streaks_sql = """       
        CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            due TEXT NOT NULL,
            action TEXT NOT NULL,
            time TEXT,
            completed INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now')),
            ended_at TEXT DEFAULT NULL,
            days_completed INTEGER NOT NULL DEFAULT 0
        )
        """

        execute_sql(conn, "Create goals table", goals_sql)
        execute_sql(conn, "Create streaks table", streaks_sql)

        conn.commit()
