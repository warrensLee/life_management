from datetime import date, timedelta

from backend.database import get_conn
from backend.classes.streaks import Streak
from backend.services import parse_due_date

''' ------------------------------- streak themes ------------------------------- '''

STREAK_THEMES = {
    "default": {
        "complete": "#E47F51",
        "incomplete": "#51E484"
    },

    "ocean": {
        "complete": "#3BA7FF",
        "incomplete": "#FF9B6A"
    },

    "sunset": {
        "complete": "#FF8A5B",
        "incomplete": "#5BA8FF"
    },

    "violet": {
        "complete": "#B084FF",
        "incomplete": "#FFD166"
    }
}

''' ------------------------------- helper streaks methods ------------------------------- '''


def add_streak(title: str, desc: str, days: int, due: date, theme_name: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO streaks(title, description, days_completed, due, theme_name)
            VALUES (?, ?, ?, ?, ?)
            """,
            (title, desc, days, due, theme_name),
        )
        conn.commit()
        return cur.lastrowid

def list_streaks(include_completed=True) -> list[Streak]:
    q = """
        SELECT id, title, description,
               created_at, updated_at, ended_at,
               completed, days_completed, theme_name
        FROM streaks
    """

    if not include_completed:
        q += " WHERE completed = 0"

    q += " ORDER BY id DESC"

    with get_conn() as conn:
        rows = conn.execute(q).fetchall()

    out = []

    for row in rows:
        sid, title, desc, created_at, updated_at, ended_at, completed, days_completed, theme_name = row

        out.append(
            Streak(
                id=sid,
                title=title,
                description=desc,
                created_at=parse_due_date(created_at),
                updated_at=parse_due_date(updated_at),
                ended_at=parse_due_date(ended_at) if ended_at else None,
                completed=bool(completed),
                days_completed=days_completed,
                theme_name=theme_name,
            )
        )

    return out


def set_streaks_completed(streaks_id: int, completed: bool):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE streaks
            SET completed = ?, updated_at = datetime('now')
            WHERE id = ?
            """,
            (1 if completed else 0, streaks_id),
        )
        conn.commit()


def delete_streak(streak_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM streaks WHERE id = ?", (streak_id,))
        conn.commit()

def increment_streak(streak_id: int):
    with get_conn() as conn:
        conn.execute("""
                UPDATE streaks
                set days_completed = days_completed + 1
                WHERE id = ?
            """, (streak_id,))
        conn.commit()

def decrement_streak(streak_id: int):
    with get_conn() as conn:
        conn.execute("""
                UPDATE streaks
                set days_completed = days_completed - 1
                WHERE id = ?
            """, (streak_id,))
        conn.commit()

def update_streaks(streaks_id: int, title: str, desc: str, theme_name: str):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE streaks
            SET title = ?, description = ?, updated_at = datetime('now'), theme_name = ?
            WHERE id = ?
            """,
            (title, desc, theme_name, streaks_id),
        )
        conn.commit()


def create_streaks(title: str, desc: str, theme_name: str = "default") -> int:
    if not title.strip():
        raise ValueError("Title is required.")

    return add_streak(title.strip(), desc.strip(), 0, date.today(), theme_name.strip())


''' ------------------------------- main streaks methods ------------------------------- '''


def get_streaks(include_completed=True) -> list[Streak]:
    return list_streaks(include_completed=include_completed)


def complete_streaks(streaks_id: int):
    set_streaks_completed(streaks_id, True)


def uncomplete_streaks(streaks_id: int):
    set_streaks_completed(streaks_id, False)


def remove_streak(streak_id: int):
    delete_streak(streak_id)

def get_theme(theme_name):
    return STREAK_THEMES.get(theme_name, STREAK_THEMES["default"])

def get_naive_completed_days_for_month(days_completed):
    today = date.today()
    completed_days = set()

    for i in range(days_completed):
        streak_day = today - timedelta(days=i)

        if streak_day.year == today.year and streak_day.month == today.month:
            completed_days.add(streak_day.day)

    return completed_days