from backend.routes import goal
from backend.services import parse_due_date

from tkinter import messagebox
import traceback
import customtkinter as ctk


class GoalsTab(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(row=0, column=0, sticky="nsew")

        self.parent = parent
        self.build_goals_tab()
        self.refresh()

    def build_goals_tab(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self)
        top.grid(row=0, column=0, padx=16, pady=16, sticky="ew")

        for i in range(6):
            top.grid_columnconfigure(i, weight=1)

        self.goal_font_title = ctk.CTkFont(size=18, weight="bold")
        self.goal_font_active = ctk.CTkFont(size=15, weight="normal")
        self.goal_font_completed = ctk.CTkFont(size=14, slant="italic")

        ctk.CTkLabel(top, text="Action / Behavior", font=self.goal_font_title).grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(top, text="Location", font=self.goal_font_title).grid(row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(top, text="Date (YYYY-MM-DD)", font=self.goal_font_title).grid(row=0, column=2, padx=10, pady=(10, 0), sticky="w")

        self.goal_action_entry = ctk.CTkEntry(top, placeholder_text="Run 2 miles")
        self.goal_action_entry.grid(row=1, column=0, padx=8, pady=10, sticky="ew")

        self.goal_location_entry = ctk.CTkEntry(top, placeholder_text="Gym")
        self.goal_location_entry.grid(row=1, column=1, padx=8, pady=10, sticky="ew")

        self.goal_date_entry = ctk.CTkEntry(top, placeholder_text="2026-02-01")
        self.goal_date_entry.grid(row=1, column=2, padx=8, pady=10, sticky="ew")

        ctk.CTkButton(top, text="Add Goal", command=self.add_goal).grid(row=1, column=3, padx=8, pady=10, sticky="ew")
        ctk.CTkButton(top, text="Refresh", command=self.refresh).grid(row=1, column=4, padx=8, pady=10, sticky="ew")

        self.show_completed = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(top, text="Show completed", variable=self.show_completed, command=self.refresh).grid(row=1, column=5, padx=8, pady=8, sticky="e")

        mid = ctk.CTkFrame(self)
        mid.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_rowconfigure(0, weight=1)

        self.goal_list_frame = ctk.CTkScrollableFrame(mid)
        self.goal_list_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        self.goal_rows = []

    def refresh(self):
        self.goal_refresh()

    def goal_refresh(self):
        for _, _, row in self.goal_rows:
            row.destroy()

        self.goal_rows.clear()

        goals = goal.get_goals(include_completed=self.show_completed.get())

        for g in goals:
            row = ctk.CTkFrame(self.goal_list_frame)
            row.pack(fill="x", padx=6, pady=6)

            done_var = ctk.BooleanVar(value=g.completed)

            chk = ctk.CTkCheckBox(
                row,
                text="",
                variable=done_var,
                command=lambda gid=g.id, v=done_var: self.toggle_goal_complete(gid, v)
            )
            chk.pack(side="left", padx=(10, 6))

            goal_lbl = ctk.CTkLabel(
                row,
                text=g.display(),
                anchor="w",
                font=self.goal_font_completed if g.completed else self.goal_font_active,
                text_color="#9ca3af" if g.completed else None
            )
            goal_lbl.pack(side="left", padx=6, fill="x", expand=True)

            del_btn = ctk.CTkButton(
                row,
                text="Delete",
                width=70,
                command=lambda gid=g.id: self.delete_goal(gid)
            )
            del_btn.pack(side="right", padx=10)

            self.goal_rows.append((g.id, done_var, row))

    def add_goal(self):
        act = self.goal_action_entry.get().strip()
        loc = self.goal_location_entry.get().strip()
        due = self.goal_date_entry.get().strip()

        try:
            due = parse_due_date(due)
            goal.add_goal(loc, due, act)
        except ValueError as e:
            messagebox.showwarning("Invalid", str(e))
            return
        except Exception as e:
            print("Error while adding goal:", e)
            traceback.print_exc()
            messagebox.showwarning("Invalid", str(e))
            return

        self.goal_location_entry.delete(0, "end")
        self.goal_date_entry.delete(0, "end")
        self.goal_action_entry.delete(0, "end")
        self.refresh()

    def toggle_goal_complete(self, goal_id, var):
        goal.set_goal_completed(goal_id, var.get())
        self.refresh()

    def delete_goal(self, goal_id):
        goal.remove_goal(goal_id)
        self.refresh()