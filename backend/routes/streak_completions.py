from datetime import date, timedelta

from backend.database import get_conn
from backend.classes.streak_completions import Streak_Completions
from backend.services import parse_due_date

''' ------------------------------- main streak completions methods ------------------------------- '''

def complete_streak(streak_id: int, completed_date: date) -> int:
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT OR IGNORE INTO streak_completions(streak_id, completed_date)
            VALUES (?, ?)
            """,
            (streak_id, completed_date.isoformat()),
        )
        conn.commit()
        return cur.lastrowid

def uncomplete_streak(streak_id: int, completed_date: date):
    with get_conn() as conn:
        conn.execute("""
            DELETE FROM streak_completions 
            WHERE streak_id = ? 
            AND completed_date = ?
            """, 
        (streak_id, completed_date.isoformat(),)
        )
        conn.commit()

def get_completed_days(streak_id: int, year: int, month: int): 
    # day is irrelevant for this, so lets
    # normalize it as 1 for consistency
    # so this will get that specific month
    # for the calendar
    start_date = date(year, month, 1)

    # what does this do?:
    # this gets the end of that specific month
    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    with get_conn() as conn:
        rows = conn.execute("""
            SELECT completed_date
            FROM streak_completions 
            WHERE streak_id = ?
            AND completed_date >= ?
            AND completed_date < ?
            ORDER BY completed_date
        """,
        (streak_id, start_date.isoformat(), end_date.isoformat())
        ).fetchall()
    
    return [
            parse_due_date(row["completed_date"])
            for row in rows
        ]

def get_all_completed(streak_id: int):
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT completed_date
            FROM streak_completions 
            WHERE streak_id = ? 
            """, 
        (streak_id,)
        ).fetchall()
        conn.commit()

    return {
        row["completed_date"]
        for row in rows
    }

def get_current_streak(streak_id: int) -> int:
    completed_dates = get_all_completed(streak_id)
    # this will get the current streak the
    # user is in (consecutively).
    current = date.today()

    # if today is not done yet, don't punish the user.
    # start counting from yesterday instead.
    if current.isoformat() not in completed_dates:
        current -= timedelta(days=1)

    count = 0

    # count the days in order 
    while current.isoformat() in completed_dates:
        count += 1
        current -= timedelta(days=1)

    return count

# this will remain incomplete for a while,
# as it is not required. I would like to
# use partitoning to implement a solution
# in the future.
def get_longest_streak(streak_id: int):
    pass

''' ------------------------------- helper streak completions methods ------------------------------- '''
