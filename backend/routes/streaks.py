from datetime import date

from backend.database import get_conn
from backend.classes.streaks import Streak
from backend.services import parse_due_date


''' ------------------------------- helper streak methods ------------------------------- '''

def add_streak(location: str, due: date, action: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO streaks(location, due, action, completed) VALUES(?,?,?,0)",
            (location, due.isoformat(), action),
        )
        conn.commit()
        return cur.lastrowid


def list_streaks(include_completed=True) -> list[Streak]:
    q = "SELECT id, location, due, action, completed FROM streaks"
    params = ()
    if not include_completed:
        q += " WHERE completed = 0"
    q += " ORDER BY due ASC, id DESC"

    with get_conn() as conn:
        rows = conn.execute(q, params).fetchall()

    out = []
    for gid, loc, due_str, act, comp in rows:
        y, m, d = map(int, due_str.split("-"))
        out.append(Streak(gid, loc, date(y, m, d), act, bool(comp)))
    return out


def set_streak_completed(streak_id: int, completed: bool):
    with get_conn() as conn:
        conn.execute(
            "UPDATE streaks SET completed = ?, updated_at = datetime('now') WHERE id = ?",
            (1 if completed else 0, streak_id),
        )
        conn.commit()


def delete_streak(streak_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM streaks WHERE id = ?", (streak_id,))
        conn.commit()


def update_streak(streak_id: int, location: str, due: date, action: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE streaks SET location = ?, due = ?, action = ?, updated_at = datetime('now') WHERE id = ?",
            (location, due.isoformat(), action, streak_id),
        )
        conn.commit()


def create_streak(location: str, due_str: str, action: str) -> int:
    if not location.strip():
        raise ValueError("Location is required.")
    if not action.strip():
        raise ValueError("Action/behavior is required.")
    due = parse_due_date(due_str)
    return add_streak(location.strip(), due, action.strip())


''' ------------------------------- main streak methods ------------------------------- '''

def get_streaks(include_completed=True) -> list[Streak]:
    return list_streaks(include_completed=include_completed)


def complete_streak(streak_id: int):
    set_streak_completed(streak_id, True)


def uncomplete_streak(streak_id: int):
    set_streak_completed(streak_id, False)


def remove_streak(streak_id: int):
    delete_streak(streak_id)
