from datetime import date

from backend.database import get_conn
from backend.classes.goal import Goal
from backend.services import parse_due_date


''' ------------------------------- helper goal methods ------------------------------- '''

def add_goal(location: str, due: date, action: str) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO goals(location, due, action, completed) VALUES(?,?,?,0)",
            (location, due, action),
        )
        conn.commit()
        return cur.lastrowid


def list_goals(include_completed=True) -> list[Goal]:
    q = "SELECT id, location, due, action, completed FROM goals"
    params = ()
    if not include_completed:
        q += " WHERE completed = 0"
    q += " ORDER BY due ASC, id DESC"

    with get_conn() as conn:
        rows = conn.execute(q, params).fetchall()

    out = []
    for gid, loc, due_str, act, comp in rows:
        y, m, d = map(int, due_str.split("-"))
        out.append(Goal(gid, loc, date(y, m, d), act, bool(comp)))
    return out


def set_goal_completed(goal_id: int, completed: bool):
    with get_conn() as conn:
        conn.execute(
            "UPDATE goals SET completed = ?, updated_at = datetime('now') WHERE id = ?",
            (1 if completed else 0, goal_id),
        )
        conn.commit()


def delete_goal(goal_id: int):
    with get_conn() as conn:
        conn.execute("DELETE FROM goals WHERE id = ?", (goal_id,))
        conn.commit()


def update_goal(goal_id: int, location: str, due: date, action: str):
    with get_conn() as conn:
        conn.execute(
            "UPDATE goals SET location = ?, due = ?, action = ?, updated_at = datetime('now') WHERE id = ?",
            (location, due.isoformat(), action, goal_id),
        )
        conn.commit()


def create_goal(location: str, due_str: str, action: str) -> int:
    if not location.strip():
        raise ValueError("Location is required.")
    if not action.strip():
        raise ValueError("Action/behavior is required.")
    due = parse_due_date(due_str)
    return add_goal(location.strip(), due, action.strip())


''' ------------------------------- main goal methods ------------------------------- '''

def get_goals(include_completed=True) -> list[Goal]:
    return list_goals(include_completed=include_completed)


def complete_goal(goal_id: int):
    set_goal_completed(goal_id, True)


def uncomplete_goal(goal_id: int):
    set_goal_completed(goal_id, False)


def remove_goal(goal_id: int):
    delete_goal(goal_id)
