# app.py
import customtkinter as ctk
from tkinter import messagebox

from backend import database
from backend import services
from backend.classes import goal, personality, habits, streaks
from backend.routes import goal

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Life Manager V1")
        self.geometry("1280x720")

        database.init_db()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- Tabs (top navigation) ---
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=16, pady=16, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)   # tabview takes the whole window
        self.grid_columnconfigure(0, weight=1)

        goals_tab = self.tabs.add("Goals")
        personality_tab = self.tabs.add("Personality")
        habits_tab = self.tabs.add("Habits")
        streaks_tab = self.tabs.add("Streaks")

        # Build each tab UI
        self.build_goals_tab(goals_tab)
        self.build_personality_tab(personality_tab)
        self.build_habits_tab(habits_tab)
        self.build_streaks_tab(streaks_tab)

        self.refresh()

    def on_add(self):
        act = self.action_entry.get()
        loc = self.location_entry.get()
        due = self.date_entry.get()

        try:
            services.create_goal(loc, due, act)
        except ValueError as e:
            messagebox.showwarning("Invalid", str(e))
            return
        except Exception:
            messagebox.showwarning("Invalid", "Date must be YYYY-MM-DD.")
            return

        self.location_entry.delete(0, "end")
        self.date_entry.delete(0, "end")
        self.action_entry.delete(0, "end")

        self.refresh()

    def refresh(self):
        # clear existing rows
        for _, _, row in self.rows:
            row.destroy()
        self.rows.clear()

        goals = goal.get_goals(include_completed=self.show_completed.get())

        for g in goals:
            row = ctk.CTkFrame(self.list_frame)
            row.pack(fill="x", padx=6, pady=6)

            done_var = ctk.BooleanVar(value=g.completed)
            chk = ctk.CTkCheckBox(row, text="", variable=done_var,
                                  command=lambda gid=g.id, v=done_var: self.toggle_complete(gid, v))
            chk.pack(side="left", padx=(10, 6))

            lbl = ctk.CTkLabel(row, text=g.display(), anchor="w", font=self.goal_font_completed if g.completed
                               else self.goal_font_active, text_color="#9ca3af" if g.completed else None)
            lbl.pack(side="left", padx=6, fill="x", expand=True)

            del_btn = ctk.CTkButton(
                row, text="Delete", width=70, command=lambda gid=g.id: self.delete_goal(gid))
            del_btn.pack(side="right", padx=10)

            self.rows.append((g.id, done_var, row))

    def toggle_complete(self, goal_id, var):
        try:
            if var.get():
                services.complete_goal(goal_id)
            else:
                services.uncomplete_goal(goal_id)
        finally:
            self.refresh()

    def delete_goal(self, goal_id):
        services.remove_goal(goal_id)
        self.refresh()

    def build_goals_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        # Top input panel
        top = ctk.CTkFrame(parent)
        top.grid(row=0, column=0, padx=16, pady=16, sticky="ew")
        for i in range(6):
            top.grid_columnconfigure(i, weight=1)

        self.font_title = ctk.CTkFont(size=18, weight="bold")
        self.font_label = ctk.CTkFont(size=14)
        self.font_entry = ctk.CTkFont(size=14)
        self.font_button = ctk.CTkFont(size=14, weight="bold")
        self.goal_font_active = ctk.CTkFont(size=15, weight="normal")
        self.goal_font_completed = ctk.CTkFont(size=14, slant="italic")

        ctk.CTkLabel(top, text="Action / Behavior", font=self.font_title).grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(top, text="Location", font=self.font_title).grid(
            row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(top, text="Date (YYYY-MM-DD)", font=self.font_title).grid(
            row=0, column=2, padx=10, pady=(10, 0), sticky="w")

        self.action_entry = ctk.CTkEntry(top, placeholder_text="Run 2 miles")
        self.action_entry.grid(row=1, column=0, padx=8, pady=10, sticky="ew")

        self.location_entry = ctk.CTkEntry(top, placeholder_text="Gym")
        self.location_entry.grid(row=1, column=1, padx=8, pady=10, sticky="ew")

        self.date_entry = ctk.CTkEntry(top, placeholder_text="2026-02-01")
        self.date_entry.grid(row=1, column=2, padx=8, pady=10, sticky="ew")

        add_btn = ctk.CTkButton(top, text="Add Goal", command=self.on_add)
        add_btn.grid(row=1, column=3, padx=8, pady=10, sticky="ew")

        refresh_btn = ctk.CTkButton(top, text="Refresh", command=self.refresh)
        refresh_btn.grid(row=1, column=4, padx=8, pady=10, sticky="ew")

        self.show_completed = ctk.BooleanVar(value=True)
        show_chk = ctk.CTkCheckBox(
            top, text="Show completed", variable=self.show_completed, command=self.refresh)
        show_chk.grid(row=1, column=5, padx=8, pady=8, sticky="e")

        # Scrollable goals list
        mid = ctk.CTkFrame(parent)
        mid.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_rowconfigure(0, weight=1)

        self.list_frame = ctk.CTkScrollableFrame(mid)
        self.list_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        self.rows = []  # store tuples: (goal_id, completed_var, row_frame)

    def build_personality_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(parent, text="Personality", font=ctk.CTkFont(size=22, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=8, pady=(8, 4)
        )

        ctk.CTkLabel(parent, text="Put your personality tracker/settings here.").grid(
            row=1, column=0, sticky="w", padx=8, pady=4
        )

        # Example input
        self.personality_entry = ctk.CTkEntry(
            parent, placeholder_text="e.g., 'Be consistent', 'Be calm'")
        self.personality_entry.grid(
            row=2, column=0, sticky="ew", padx=8, pady=8)

        ctk.CTkButton(parent, text="Save", command=lambda: print(self.personality_entry.get())).grid(
            row=3, column=0, sticky="w", padx=8, pady=8
        )

    def build_habits_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        pass

    def build_streaks_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        pass

def run():
    App().mainloop()
