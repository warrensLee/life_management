# app.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import date
import traceback

from backend import database
from backend import services
from backend.classes import goal, streaks
from backend.routes import goal, streaks

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("core/app_theme.json")


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
        streaks_tab = self.tabs.add("Streaks")

        # Build each tab UI
        self.build_goals_tab(goals_tab)
        self.build_streaks_tab(streaks_tab)

        self.refresh()

    def add_goal(self):
        act = self.goal_action_entry.get().strip()
        loc = self.goal_location_entry.get().strip()
        due = self.goal_date_entry.get().strip()

        try:
            due = date.fromisoformat(due)
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

    def add_streak(self):
        title = self.streak_title_entry.get().strip()
        desc = self.streak_description_entry.get().strip()
        days = self.streak_days_entry.get().strip()
        due = self.streak_date_entry.get().strip()

        try:
            due = date.fromisoformat(due)
            streaks.add_streak(title, desc, days, due)
        except ValueError as e:
            messagebox.showwarning("Invalid", str(e))
            return
        except Exception as e:
            print("Error while adding streak:", e)
            traceback.print_exc()
            messagebox.showwarning("Invalid", str(e))
            return

        self.streak_title_entry.delete(0, "end")
        self.streak_description_entry.delete(0, "end")
        self.streak_days_entry.delete(0, "end")
        self.streak_date_entry.delete(0, "end")


    def on_add(self):
        self.add_goal()
        self.add_streak()
        self.refresh()

    def goal_refresh(self):
        # clear existing rows
        for _, _, row in self.goal_rows:
            row.destroy()
        self.goal_rows.clear()

        goals = goal.get_goals(include_completed=self.show_completed.get())
        for g in goals:
            row = ctk.CTkFrame(self.goal_list_frame)
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

            self.goal_rows.append((g.id, done_var, row))

    def streak_refresh(self):
        # clear existing rows
        for _, _, row in self.streak_rows:
            row.destroy()
        self.streak_rows.clear()

        all_streaks = streaks.get_streaks(include_completed=self.show_completed.get())
        for g in all_streaks:
            row = ctk.CTkFrame(self.streak_list_frame)
            row.pack(fill="x", padx=6, pady=6)

            done_var = ctk.BooleanVar(value=g.completed)
            chk = ctk.CTkCheckBox(row, text="", variable=done_var,
                                  command=lambda gid=g.id, v=done_var: self.toggle_complete(gid, v))
            chk.pack(side="left", padx=(10, 6))

            lbl = ctk.CTkLabel(row, text=g.display(), anchor="w", font=self.streak_font_completed if g.completed
                else self.streak_font_active, text_color="#9ca3af" if g.completed else None)
            lbl.pack(side="left", padx=6, fill="x", expand=True)

            del_btn = ctk.CTkButton(
                row, text="Delete", width=70, command=lambda gid=g.id: self.delete_streak(gid))
            del_btn.pack(side="right", padx=10)

            self.streak_rows.append((g.id, done_var, row))
    
            
    def refresh(self):
        self.goal_refresh()
        self.streak_refresh()  # TODO: implement streak refresh similar to goal_refresh

    def toggle_complete(self, goal_id, var):
        try:
            if var.get():
                goal.set_goal_completed(goal_id, True)
            else:
                goal.set_goal_completed(goal_id, False)
        finally:
            self.refresh()

    def delete_goal(self, goal_id):
        goal.remove_goal(goal_id)
        self.refresh()

    def build_goals_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        # Top input panel
        top = ctk.CTkFrame(parent)
        top.grid(row=0, column=0, padx=16, pady=16, sticky="ew")
        for i in range(6):
            top.grid_columnconfigure(i, weight=1)

        self.goal_font_title = ctk.CTkFont(size=18, weight="bold")
        self.goal_font_label = ctk.CTkFont(size=14)
        self.goal_font_entry = ctk.CTkFont(size=14)
        self.goal_font_button = ctk.CTkFont(size=14, weight="bold")
        self.goal_font_active = ctk.CTkFont(size=15, weight="normal")
        self.goal_font_completed = ctk.CTkFont(size=14, slant="italic")

        ctk.CTkLabel(top, text="Action / Behavior", font=self.goal_font_title).grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(top, text="Location", font=self.goal_font_title).grid(
            row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        ctk.CTkLabel(top, text="Date (YYYY-MM-DD)", font=self.goal_font_title).grid(
            row=0, column=2, padx=10, pady=(10, 0), sticky="w")

        self.goal_action_entry = ctk.CTkEntry(top, placeholder_text="Run 2 miles")
        self.goal_action_entry.grid(row=1, column=0, padx=8, pady=10, sticky="ew")

        self.goal_location_entry = ctk.CTkEntry(top, placeholder_text="Gym")
        self.goal_location_entry.grid(row=1, column=1, padx=8, pady=10, sticky="ew")

        self.goal_date_entry = ctk.CTkEntry(top, placeholder_text="2026-02-01")
        self.goal_date_entry.grid(row=1, column=2, padx=8, pady=10, sticky="ew")

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

        self.goal_list_frame = ctk.CTkScrollableFrame(mid)
        self.goal_list_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        self.goal_rows = []  # store tuples: (goal_id, completed_var, row_frame)

    def build_streaks_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)
        # Top input panel
        top = ctk.CTkFrame(parent)
        top.grid(row=0, column=0, padx=16, pady=16, sticky="ew")
        for i in range(6):
            top.grid_columnconfigure(i, weight=1)

        self.streak_font_title = ctk.CTkFont(size=18, weight="bold")
        self.streak_font_label = ctk.CTkFont(size=14)
        self.streak_font_entry = ctk.CTkFont(size=14)
        self.streak_font_button = ctk.CTkFont(size=14, weight="bold")
        self.streak_font_active = ctk.CTkFont(size=15, weight="normal")
        self.streak_font_completed = ctk.CTkFont(size=14, slant="italic")

        # input sections, their title and stylization
        ctk.CTkLabel(top, text="Title", font=self.streak_font_title).grid(
            row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        
        ctk.CTkLabel(top, text="Description", font=self.streak_font_title).grid(
            row=0, column=1, padx=10, pady=(10, 0), sticky="w")
        
        ctk.CTkLabel(top, text="Days Already Completed", font=self.streak_font_title).grid(
            row=0, column=2, padx=10, pady=(10, 0), sticky="w")
        
        ctk.CTkLabel(top, text="Start Date (YYYY-MM-DD)", font=self.streak_font_title).grid(
            row=0, column=3, padx=10, pady=(10, 0), sticky="w")
        
        # now for placeholder text and entry points
        self.streak_title_entry = ctk.CTkEntry(top, placeholder_text="Sleep On Time")
        self.streak_title_entry.grid(row=1, column=0, padx=8, pady=10, sticky="ew")

        self.streak_description_entry = ctk.CTkEntry(top, placeholder_text="Go to bed by 11:00 PM")
        self.streak_description_entry.grid(row=1, column=1, padx=8, pady=10, sticky="ew")

        self.streak_days_entry = ctk.CTkEntry(top, placeholder_text="3")
        self.streak_days_entry.grid(row=1, column=2, padx=8, pady=10, sticky="ew")

        self.streak_date_entry = ctk.CTkEntry(top, placeholder_text="2026-02-01")
        self.streak_date_entry.grid(row=1, column=3, padx=8, pady=10, sticky="ew")

        add_btn = ctk.CTkButton(top, text="Add Streak", command=self.on_add)
        add_btn.grid(row=1, column=4, padx=8, pady=10, sticky="ew")

        refresh_btn = ctk.CTkButton(top, text="Refresh", command=self.refresh)
        refresh_btn.grid(row=1, column=5, padx=8, pady=10, sticky="ew")

        # Scrollable streaks list
        mid = ctk.CTkFrame(parent)
        mid.grid(row=1, column=0, padx=16, pady=(0, 16), sticky="nsew")
        mid.grid_columnconfigure(0, weight=1)
        mid.grid_rowconfigure(0, weight=1)

        self.streak_list_frame = ctk.CTkScrollableFrame(mid)
        self.streak_list_frame.grid(row=0, column=0, padx=12, pady=12, sticky="nsew")

        self.streak_rows = []  # store tuples: (streak_id, completed_var, row_frame)

def run():
    App().mainloop()
