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

# to manage changes for the database we must be able to migrate old data -> new schema
def column_exists(conn, table_name, column_name):
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return any(row[1] == column_name for row in rows)


def migrate_db(conn):
    if not column_exists(conn, "streaks", "theme_name"):
        execute_sql(
            conn,
            "Add theme_name column to streaks",
            "ALTER TABLE streaks ADD COLUMN theme_name TEXT DEFAULT 'default'"
        )

    conn.commit()

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
            due TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            completed INTEGER DEFAULT 0,
            days_completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            ended_at TEXT,
            theme_name TEXT DEFAULT 'default'
        )
        """
        streaks_completions_sql = """       
        CREATE TABLE IF NOT EXISTS streak_completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            streak_id INT NOT NULL,
            completed_date TEXT NOT NULL,
            UNIQUE (streak_id, completed_date),
            FOREIGN KEY (streak_id) REFERENCES streaks(id)
        )
        """

        execute_sql(conn, "Create goals table", goals_sql)
        execute_sql(conn, "Create streaks table", streaks_sql)
        execute_sql(conn, "Create streaks completion table", streaks_completions_sql)

        migrate_db(conn)

        conn.commit()

