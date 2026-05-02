from datetime import date, time

from backend.database import get_conn
from backend.classes.streaks import Streak
from backend.services import parse_due_date


''' ------------------------------- helper streaks methods ------------------------------- '''


def add_streak(title: str, desc: str, days: int, due: date) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO streaks(title, description, days_completed, due)
            VALUES (?, ?, ?, ?)
            """,
            (title, desc, days, due),
        )
        conn.commit()
        return cur.lastrowid

def list_streaks(include_completed=True) -> list[Streak]:
    q = """
        SELECT id, title, description,
               created_at, updated_at, ended_at,
               completed, days_completed
        FROM streaks
    """

    if not include_completed:
        q += " WHERE completed = 0"

    q += " ORDER BY id DESC"

    with get_conn() as conn:
        rows = conn.execute(q).fetchall()

    out = []

    for row in rows:
        sid, title, desc, created_at, updated_at, ended_at, completed, days_completed = row

        out.append(
            Streak(
                id=sid,
                title=title,
                description=desc,
                created_at=parse_due_date(created_at),
                updated_at=parse_due_date(updated_at),
                ended_at=parse_due_date(ended_at) if ended_at else None,
                completed=completed,
                days_completed=days_completed,
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

def update_streaks(streaks_id: int, title: str, desc: str):
    with get_conn() as conn:
        conn.execute(
            """
            UPDATE streaks
            SET title = ?, description = ?, updated_at = datetime('now')
            WHERE id = ?
            """,
            (title, desc, streaks_id),
        )
        conn.commit()


def create_streaks(title: str, desc: str) -> int:
    if not title.strip():
        raise ValueError("Title is required.")

    return add_streak(title.strip(), desc.strip())


''' ------------------------------- main streaks methods ------------------------------- '''


def get_streaks(include_completed=True) -> list[Streak]:
    return list_streaks(include_completed=include_completed)


def complete_streaks(streaks_id: int):
    set_streaks_completed(streaks_id, True)


def uncomplete_streaks(streaks_id: int):
    set_streaks_completed(streaks_id, False)


def remove_streak(streak_id: int):
    delete_streak(streak_id)